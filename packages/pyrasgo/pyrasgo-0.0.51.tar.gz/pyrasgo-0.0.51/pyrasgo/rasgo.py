from types import FunctionType
from typing import Union, List, Optional, Dict

import pandas as pd
from datetime import datetime
from deprecated import deprecated
from requests.exceptions import HTTPError
from snowflake import connector as snowflake
from snowflake.connector import SnowflakeConnection
from snowflake.connector.pandas_tools import write_pandas
import yaml

from pyrasgo.connection import Connection
from pyrasgo.enums import Granularity, ModelType
from pyrasgo.feature import Feature, FeatureList
from pyrasgo.model import Model
from pyrasgo.member import Member
from pyrasgo.monitoring import track_usage
from pyrasgo.utils import dataframe, ingestion
from pyrasgo import schemas as api


class Rasgo(Connection):
    """
    Base connection object to handle interactions with the Rasgo API.

    Defaults to using the production Rasgo instance, which can be overwritten
    by specifying the `RASGO_DOMAIN` environment variable, eg:

    &> RASGO_DOMAIN=custom.rasgoml.com python
    >>> from pyrasgo import Rasgo
    >>> rasgo = Connection(api_key='not_a_key')
    >>> rasgo._hostname == 'custom.rasgoml.com'
    True

    """
    from pyrasgo.version import __version__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @track_usage
    def create_model(self, name: str,
                     type: Union[str, ModelType],
                     granularity: Union[str, Granularity],
                     description: Optional[str] = None,
                     is_shared: Optional[bool] = False) -> Model:
        """
        Creates model within Rasgo within the account specified by the API key.
        :param name: Model name
        :param model_type: Type of model specified
        :param granularity: Granularity of the data.
        :param is_shared: True = make model shared , False = make model private
        :return: Model object.
        """
        try:
            # If not enum, convert to enum first.
            model_type = type.name
        except AttributeError:
            model_type = ModelType(type)

        try:
            # If not enum, convert to enum first.
            granularity = granularity.name
        except AttributeError:
            granularity = Granularity(granularity)

        content = {"name": name,
                   "type": model_type.value,
                   "granularities": [{"name": granularity.value}],
                   "isShared": is_shared
                   }
        if description:
            content["description"] = description
        response = self._post("/models", _json=content, api_version=1)
        return Model(api_object=response.json())

    @track_usage
    def add_feature_to(self, model: Model, feature: Feature):
        model.add_feature(feature)

    @track_usage
    def add_features_to(self, model: Model, features: FeatureList):
        model.add_features(features)

    @track_usage
    def generate_training_data_for(self, model: Model):
        raise NotImplementedError

    @track_usage
    def get_models(self) -> List[Model]:
        """
        Retrieves the list of models from Rasgo within the account specified by the API key.
        """
        return [Model(api_object=entry) for entry in self._get(f"/models", api_version=1).json()]

    @track_usage
    def get_shared_models(self) -> List[Model]:
        """
        Get all of my organizations shared models
        """
        return [Model(api_object=entry) for entry in self._get(f'/models/shared', api_version=1).json()]

    @track_usage
    def get_model(self, model_id) -> Model:
        """
        Retrieves the specified model from Rasgo within the account specified by the API key.
        """
        return Model(api_object=self._get(f"/models/{model_id}", api_version=1).json())

    @track_usage
    def get_feature(self, feature_id: int) -> Feature:
        """
        Retrieves the specified feature from Rasgo within the account specified by the API key.
        """
        response = self._get(f"/features/{feature_id}", api_version=1)
        return Feature(api_object=response.json())

    @track_usage
    def get_features(self) -> FeatureList:
        """
        Retrieves the features from Rasgo within account specified by the API key.
        """
        return FeatureList(api_object=self._get("/features", api_version=1).json())

    @track_usage
    def get_feature_stats(self, feature_id: int):
        """
        Retrieves the stats profile for a specified feature.
        """
        try:
            stats_json = self._get(f"/features/{feature_id}/stats", api_version=1).json()
        except:
            return 'Cannot find stats for this feature'
        return api.FeatureStats(**stats_json['featureStats']) or None

    @track_usage
    def post_feature_stats(self, feature_id: int):
        """
        Sends an api request to build feature stats for a specified feature.
        """
        return self._post(f'/features/{feature_id}/stats', api_version=1).json()

    @track_usage
    def get_features_for(self, model: Model) -> FeatureList:
        raise NotImplementedError()
        # response = self._get("/features",
        #                      params={'join': f""})
        #                    # params={'filter': f"||eq||DateTime"})
        # return FeatureList(response.json())

    @track_usage
    def get_feature_data(self, model_id: int,
                         filters: Optional[Dict[str, str]] = None,
                         limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs the pandas dataframe for the specified model.

        :param model_id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        model = self.get_model(model_id)

        conn, creds = self._snowflake_connection(model.get_author())

        table_metadata = model.snowflake_table_metadata(creds)
        query, values = self._make_select_statement(table_metadata, filters, limit)

        result_set = self._run_query(conn, query, values)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_feature_sets(self):
        """
        Retrieves the feature sets from Rasgo within account specified by the API key.
        """
        return self._get("/feature-sets").json()

    @track_usage
    def get_feature_set(self, feature_set_id: int):
        """
        Retrieves a feature set from Rasgo by id.
        """
        return self._get(f"/feature-sets/{feature_set_id}").json()

    @track_usage
    def get_source_tables(self):
        '''
        Retrieves a list of Snowflake tables and views that are queryable as feature sources
        '''
        conn, creds = self._snowflake_connection(self.get_member())
        query = 'SELECT * FROM RASGO_DATA_SOURCE_TABLES'
        result_set = self._run_query(conn, query, None)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_source_table(self, table_name: str, record_limit: int):
        '''
        Returns top n records from a Snowflake source table to a dataframe
        '''
        conn, creds = self._snowflake_connection(self.get_member())
        if record_limit == -1:
            query = f'SELECT * FROM {table_name}'
        else:
            query = f'SELECT * FROM {table_name} limit {record_limit}'
        result_set = self._run_query(conn, query, None)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_source_columns(self):
        '''
        Retrieves a list of columns in Snowflake tables and views that are queryable as feature sources
        '''
        conn, creds = self._snowflake_connection(self.get_member())
        query = 'SELECT * FROM RASGO_DATA_SOURCE_COLUMNS'
        result_set = self._run_query(conn, query, None)
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_data_sources(self):
        """
        Retrieves the data sources from Rasgo within account specified by the API key.
        """
        return self._get("/data-source").json()

    @track_usage
    def get_dimensionalities(self):
        """
        Retrieves the data sources from Rasgo within account specified by the API key.
        """
        return self._get("/dimensionalities").json()

    @track_usage
    def get_datasource(self, name):
        rows = self.find("data-source", {"name": name})
        if 0 == len(rows):
            return None
        else:
            return rows[0]

    def get_member(self):
        return Member(self.get_user())

    def get_user(self):
        return self._get("/users/me", api_version=1).json()

    @track_usage
    def get_dimensionality(self, name):
        return self._get_item("dimensionalities", {"name": name}, True)

    @track_usage
    def create_column(self, name, data_type, feature_set_id, dimension_id):
        column = api.ColumnCreate(name=name, dataType=data_type,
                                  featureSet=api.v0.FeatureSetBase(id=feature_set_id),
                                  dimensionality=api.Dimensionality(id=dimension_id))
        return self._post("/rcolumns", column.dict(exclude_unset=True)).json()

    @track_usage
    def update_column(self, column_id, name, data_type, feature_set_id, dimension_id):
        column = api.ColumnUpdate(id=column_id,
                                  name=name, dataType=data_type,
                                  featureSet=api.v0.FeatureSetBase(id=feature_set_id),
                                  dimensionality=api.Dimensionality(id=dimension_id))
        return self._patch(f"rcolumns/{column_id}", column.dict(exclude_unset=True)).json()

    @track_usage
    def create_datasource(self, org_id, name):
        data_source = api.DataSourceCreate(name=name,
                                           abbreviation=name[:10].lower(),
                                           organization=api.Organization(id=org_id))
        return self._post("/data-source", data_source.dict(exclude_unset=True)).json()

    @track_usage
    def create_dimensionality(self, org_id, name, dimension_type, granularity):
        dimensionality = api.DimensionalityCreate(name=name,
                                                  dimension_type=dimension_type,
                                                  granularity=granularity,
                                                  organization=api.Organization(id=org_id))
        return self._post("/dimensionalities", dimensionality.dict(exclude_unset=True)).json()

    @track_usage
    def create_feature(self, org_id: int, featureset_id: int, name: str, code: str, description: str, column_id: int,
                       status: str, gitRepo: str, tags: Optional[List[str]] = None):
        feature = api.FeatureCreate(name=name,
                                    code=code,
                                    description=description,
                                    featureSetId=featureset_id,
                                    columnId=column_id,
                                    organizationId=org_id,
                                    orchestrationStatus=status,
                                    tags=tags or [],
                                    gitRepo=gitRepo)
        return self._post("/features", feature.dict(exclude_unset=True), api_version=1).json()

    @track_usage
    def update_feature(self, feature_id: int, org_id: int, featureset_id: int, name: str, code: str, description: str,
                       column_id: int, status: str, tags: List[str], gitRepo: str):
        feature = api.FeatureUpdate(id=feature_id,
                                    name=name,
                                    code=code,
                                    description=description,
                                    featureSetId=featureset_id,
                                    columnId=column_id,
                                    organizationId=org_id,
                                    orchestrationStatus=status,
                                    tags=tags,
                                    gitRepo=gitRepo)
        return self._patch(f"/features/{feature_id}", feature.dict(exclude_unset=True), api_version=1).json()

    @track_usage
    def create_feature_set(self, name: str, datasource_id: int, table_name: str, granularity: Optional[str] = None):
        feature_set = api.v0.FeatureSetCreate(name=name,
                                              snowflakeTable=table_name,
                                              dataSource=api.DataSourceBase(id=datasource_id),
                                              granularity=granularity)
        return self._post("feature-sets", feature_set.dict()).json()

    @track_usage
    def update_feature_set(self, feature_set_id: int, name: str, datasource_id: int, table_name: str,
                           granularity: Optional[str] = None):
        feature_set = api.v0.FeatureSetUpdate(id=feature_set_id,
                                              name=name,
                                              snowflakeTable=table_name,
                                              dataSource=api.DataSourceBase(id=datasource_id),
                                              granularity=granularity)
        return self._patch(f"feature-sets/{feature_set_id}", feature_set.dict()).json()

    @track_usage
    def publish_feature_set(self, name: str, datasource_id: int, table_name: str, granularity: Optional[str] = None):
        '''
        Creates or updates a featureset depending on existence of the defined parameters
        '''
        fs = self._get_item("feature-sets", {"snowflakeTable": table_name})
        return self.update_feature_set(fs['id'], name, datasource_id, table_name, granularity) if fs else \
            self.create_feature_set(name, datasource_id, table_name, granularity)

    @track_usage
    def publish_dimensionality(self, org_id: int, dimension_type: Optional[str] = None,
                               granularity: Optional[str] = None):
        """
        Creates or returns a dimensionality depending on existence of the defined parameters

        Dimensionality is a named pairing of a datatype and a granularity. Note in some cases the
        granularity is actually a data type.
        """
        # TODO: We should move this mapping to the Granularity enum class or behind an API
        if dimension_type is None:
            if granularity.lower() in ['second', 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']:
                dimension_type = 'DateTime'
            elif granularity.lower() in ['latlong', 'zipcode', 'fips', 'dma', 'city', 'cbg', 'county', 'state',
                                         'country']:
                dimension_type = 'Geolocation'
            else:
                dimension_type = "Custom"
        elif dimension_type.lower() == "datetime":
            dimension_type = "DateTime"
        elif dimension_type.lower() in ["geo", "geoloc", "geolocation"]:
            dimension_type = "Geolocation"
        else:
            dimension_type = dimension_type.title()
        dimensionality_name = "{} - {}".format(dimension_type, str(granularity).title())

        # Check for a 'dimensionality' record that corresponds to the the dimensions
        # datatype and granularity.
        return self.get_dimensionality(dimensionality_name) or \
               self.create_dimensionality(org_id, dimensionality_name, dimension_type, granularity)

    @track_usage
    def get_column(self, name: str, featureset_id: int):
        '''
        Returns a column matching a name in the specified featureset
        '''
        items = self._get_items("rcolumns", {"name": name})
        for i in items:
            if featureset_id == i['featureSet']['id']:
                return i
        return None

    @track_usage
    def get_features_by_featureset(self, featureset_id):
        '''
        Return the list of Features in a specific Feature Set
        '''
        response = self._get(f"/features/by-featureset/{featureset_id}", api_version=1)
        return FeatureList(api_object=response.json())

    @track_usage
    def match_feature(self, code: str, featureset_id: int):
        '''
        Returns a feature matching a name in the specified featureset
        '''
        items = self._get_items("features", {"code": code})
        for i in items:
            if featureset_id == i['column']['featureSet']['id']:
                return i
        return None

    @track_usage
    def publish_dimension(self, org_id: int, featureset_id: int, name: str, data_type: str,
                          dimension_type: Optional[str] = None, granularity: Optional[str] = None):
        '''
        Creates or updates a dimension depending on existence of the defined parameters
        '''
        dimemnsionality = self.publish_dimensionality(org_id, dimension_type, granularity)
        dimemnsionality_id = dimemnsionality['id']
        dim = self.get_column(name, featureset_id)
        return self.update_column(dim['id'], name, data_type, featureset_id, dimemnsionality_id) if dim else \
            self.create_column(name, data_type, featureset_id, dimemnsionality_id)

    @track_usage
    def publish_feature(self, org_id: int, featureset_id: int, name: str, data_type: str, code: Optional[str] = None,
                        description: Optional[str] = None, granularity: Optional[str] = None,
                        status: Optional[str] = None, tags: Optional[List[str]] = None, gitRepo: Optional[str] = None):
        '''
        Creates or updates a feature depending on existence of the defined parameters
        '''
        code = code or name
        description = description or f"Feature that contains {name} data"
        status = status or 'Sandboxed'
        dimension_id = None if granularity is None else self.publish_dimensionality(org_id, None, granularity)['id']

        ft = self.match_feature(code, featureset_id)
        if ft:
            self.update_column(ft['column']['id'], code, data_type, featureset_id, dimension_id)
            feature = self.update_feature(ft['id'], org_id, featureset_id, name, code, description, ft['column']['id'],
                                          status, tags or [], gitRepo)
        else:
            column = self.create_column(code, data_type, featureset_id, dimension_id)
            feature = self.create_feature(org_id, featureset_id, name, code, description, column['id'], status, gitRepo,
                                          tags or [])

        return feature

    @track_usage
    def publish_datasource(self, org_id: int, ds_name: str):
        '''
        Creates or returns a datasource depending on of the defined parameters
        '''
        # Check for a 'dimensionality' record that corresponds to the the dimensions
        # datatype and granularity.
        return self.get_datasource(ds_name) or self.create_datasource(org_id, ds_name)

    def _confirm_df_columns(self, dataframe: pd.DataFrame, dimensions: List[str], features: List[str]):
        df_columns = list(dataframe.columns)
        missing_dims = []
        missing_features = []
        for dim in dimensions:
            if dim not in df_columns:
                missing_dims.append(dim)
        for ft in features:
            if ft not in df_columns:
                missing_features.append(ft)
        if missing_dims or missing_features:
            raise Exception(f"Specified columns do not exist in dataframe: "
                            f"Dimensions({missing_dims}) Features({missing_features})")

    def _snowflakify_name(self, name):
        '''
        param name: string
        return: string
        Converts a string to a snowflake compliant value
        Removes double quotes, replaces dashes with underscores, casts to upper case
        '''
        return name.replace("-", "_").replace('"', '').upper()

    def _snowflakify_list(self, list_in):
        '''
        param list_in: list
        return list_out: list
        Changes a list of columns to Snowflake compliant names
        '''
        list_out = [self._snowflakify_name(n) for n in list_in]
        return list_out

    def _snowflakify_dataframe(self, df: pd.DataFrame):
        '''
        param dataframe: dataframe holding columns
        param column: list of column names that need to change
        Renames all columns in a pandas dataframe to Snowflake compliant names
        '''
        schema = dataframe.build_schema(df)
        cols = {}
        for r in schema:
            oldc = r
            newc = self._snowflakify_name(oldc)
            cols[oldc] = newc
        df.rename(columns=cols, inplace=True)

    def _dataframe_to_snowflake(self, dataframe, table_name):
        conn, creds = self._snowflake_connection(self.get_member())
        with conn.cursor() as cur:
            # Create the table in Snowflake
            tablesql = self._generate_ddl_from_dataframe(dataframe, table_name)
            cur.execute(tablesql)
        # load data from df to SF table
        write_pandas(conn, dataframe, table_name)

    def _generate_ddl_from_dataframe(self, df, table_name):
        sql_text = pd.io.sql.get_schema(df.reset_index(), table_name)
        sql_text = sql_text.replace('CREATE TABLE', 'CREATE OR REPLACE TABLE')
        sql_text = sql_text.replace('"', '')
        return sql_text

    @track_usage
    def publish_features_from_df(self, df: pd.DataFrame, dimensions: List[str], features: List[str],
                                 granularity: str = None, tags: List[str] = None):
        '''
        Creates a featureset from a pandas dataframe

        :dataframe: Pandas DataFrame containing all columns that will be registered with Rasgo
        :param dimensions: List of columns in df that should be used for joins to other featursets
        :param features: List of columns in df that should be registered as features in Rasgo
        :param granularity: Datetime grain to be added to all features in the df
        :param tags: List of tags to be added to all features in the df
        :return: description of the featureset created
        '''
        # todo: Optionally generate list of feature columns from the dataframe columns, ie - all non-dimensions are features
        # todo: Add option to specify a featureset name + add check that it exists.
        # Type checking
        if not isinstance(dimensions, list) and all([isinstance(dimension, str) for dimension in dimensions]):
            raise TypeError('Dimensions must be provided as a list of strings, naming the columns within the dataframe')
        if not isinstance(features, list) and all([isinstance(feature, str) for feature in features]):
            raise TypeError('Features must be provided as a list of strings, naming the columns within the dataframe')

        tags = tags or []
        if not isinstance(tags, list):
            raise TypeError('Tags must be provided as a list of strings')

        member = self.get_member()
        org_id = member.organization_id()
        now = datetime.now()
        timestamp = now.strftime("%Y_%m_%d_%H_%M")
        datasource = self.publish_datasource(org_id, 'PANDAS')

        # Convert all strings to work with Snowflake
        dimensions = self._snowflakify_list(dimensions)
        features = self._snowflakify_list(features)
        self._snowflakify_dataframe(df)

        # Confirm each named dimension and feature exists in the dataframe.
        self._confirm_df_columns(df, dimensions, features)

        # Generate featureset name.
        featureset_name = f"pandas_by_{'-'.join(dimensions)}_{timestamp}"

        # Create a table in Snowflake with the subset of columns we're interested in, name table after featureset.
        all_columns = dimensions + features
        exportable_df = df[all_columns]
        table_name = self._snowflakify_name(featureset_name)
        self._dataframe_to_snowflake(exportable_df, table_name)

        # Add a reference to the FeatureSet
        featureset_name = table_name
        featureset = self.create_feature_set(featureset_name, datasource['id'], table_name, granularity)
        schema = dataframe.build_schema(df)

        return_featureset = {}
        return_featureset['id'] = featureset['id']
        return_featureset['name'] = featureset['name']
        return_featureset['granularity'] = featureset['granularity']
        return_featureset['dataSource'] = featureset['dataSource']['name']
        return_featureset['organization'] = featureset['dataSource']['organization']['name']
        return_featureset['snowflakeTable'] = featureset['snowflakeTable']

        # Add references to all the dimensions
        return_dimensions = {}
        for d in dimensions:
            column = schema[d]
            data_type = column['type']
            dimension_name = column['name']
            dimension = self.publish_dimension(org_id, featureset['id'], dimension_name, data_type, None, granularity)
            return_dimensions.update({dimension['id']: {"name": dimension['name']}})
        return_featureset['dimensions'] = return_dimensions

        # Add references to all the features
        return_features = {}
        for f in features:
            column = schema[f]
            data_type = column['type']
            code = column['name']
            feature_name = f"PANDAS_{code}_{timestamp}"
            status = 'Sandboxed'
            tags.append('Pandas')
            feature = self.publish_feature(org_id, featureset['id'], feature_name, data_type, code, None, granularity,
                                           status, tags)
            self.post_feature_stats(feature['id'])
            return_features.update({feature['id']:
                                        {"id": feature['id'],
                                         "name": feature['name'],
                                         "column": feature['code']
                                         }})
        return_featureset['features'] = return_features
        return return_featureset

    @track_usage
    def prepare_feature_set(self, source_table: str, name: Optional[str] = None, *,
                            dimensions_in: List[str], features_in: List[str] = None, df: Optional[pd.DataFrame] = None,
                            granularity: Optional[str] = None, function: FunctionType = None,
                            overwrite: bool = False, directory: Optional[str] = None) -> tuple:
        """
        Assembles required files for feature set creation and orchestration

        :param source_table: Table feature set will be built off of.
        :param name: Name of the feature set (defaults to the source table name)
        :param dimensions_in: List of column names identified as dimensions for the feature set
        :param features_in: List of column names identified as features within the feature set
                            (defaults to all non-dimension columns)
        :param df: Dataframe containing data from the source table, defaults to the first 10 entries of the source table.
                   This can be provided if its already available locally.
        :param granularity: Name of the granularity of the dimension
        :param function: Function to be optionally performed on dataframe during feature generation
        :param overwrite: Boolean flag whether to overwrite any existing files within the specified directory
                          (defaults to False)
        :param directory: Optionally specify the location of the newly created files
                          (defaults to the present working directory)
        :return: description of the featureset created
        """
        if df is None:
            df = self.get_source_table(table_name=source_table, record_limit=10)

        schema = dataframe.build_schema(df)
        dimensions = [api.v1.Dimension(name=schema[dimension]['name'],
                                       data_type=api.v1.DataType(schema[dimension]['type']))
                      for dimension in dimensions_in]

        if features_in is None:
            features = [api.v1.Feature(name=schema[column]['name'],
                                       data_type=api.v1.DataType(schema[column]['type']))
                        for column in schema.keys() if schema[column]['name'] not in dimensions_in]
        else:
            features = [api.v1.Feature(name=schema[feature]['name'],
                                       data_type=api.v1.DataType(schema[feature]['type']))
                        for feature in features_in]

        feature_set = api.v1.FeatureSet(name=name, script=f"{function.__name__}.py" if function else None,
                                        dimensions=dimensions, features=features,
                                        table=source_table, granularity=granularity)

        return ingestion.generate_feature_set_files(source_table=source_table, name=name, feature_set=feature_set,
                                                    function=function, directory=directory, overwrite=overwrite)

    @staticmethod
    def _snowflake_connection(member) -> (SnowflakeConnection, dict):
        """
        Constructs connection object for Snowflake data platform
        :param member: credentials for Snowflake data platform

        :return: Connection object to use for query execution
        """
        creds = member.snowflake_creds()
        conn = snowflake.connect(**creds)
        return conn, creds

    @staticmethod
    def _make_select_statement(table_metadata: dict, filters: dict, limit: Optional[int] = None) -> tuple:
        """
        Constructs select * query for table
        """
        query = "SELECT * FROM {database}.{schema}.{table}".format(**table_metadata)
        values = []
        if filters:
            comparisons = []
            for k, v in filters.items():
                if isinstance(v, list):
                    comparisons.append(f"{k} IN ({', '.join(['%s'] * len(v))})")
                    values += v
                elif v[:1] in ['>', '<', '='] \
                        or v[:2] in ['>=', '<=', '<>', '!='] \
                        or v[:4] == 'IN (' \
                        or v[:8] == 'BETWEEN ':
                    comparisons.append(f'{k} {v}')
                else:
                    comparisons.append(f"{k}=%s")
                    values.append(v)
            query += " WHERE " + " and ".join(comparisons)
        if limit:
            query += " LIMIT {}".format(limit)
        return query, values

    @staticmethod
    @track_usage
    def _run_query(conn, query: str, params):
        """
        Execute a query on the [cloud] data platform.

        :param conn: TODO -> abstract the cloud data platform connection
        :param query: String to be executed on the data platform
        :return:
        """
        return conn.cursor().execute(query, params)

    @deprecated("This function has been deprecated, use `get_models` instead.")
    @track_usage
    def get_lists(self) -> List[Model]:
        """
        Deprecated function.  Renamed to `get_models.`
        """
        return self.get_models()

    @deprecated("This function has been deprecated, use `get_model` instead.")
    @track_usage
    def get_feature_list(self, list_id) -> Model:
        """
        Deprecated function.  Renamed to `get_model.`
        """
        return self.get_model(model_id=list_id)
