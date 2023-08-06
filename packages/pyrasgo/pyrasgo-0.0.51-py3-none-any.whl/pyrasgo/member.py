import os


class Member(object):

    def __init__(self, api_object):
        self._api_object = api_object

    def organization_id(self):
        return self._api_object["organizationId"]

    def snowflake_creds(self):
        org = self._api_object.get("organization", {})
        user = self._api_object.get("snowUsername", os.environ.get('SNOWFLAKE_USERNAME', None))
        return {
            "user": user,
            "password": self._api_object.get("snowPassword", os.environ.get('SNOWFLAKE_PASSWORD')),
            "account": org.get("account", os.environ.get("SNOWFLAKE_ACCOUNT")),
            "database": org.get("database", os.environ.get("SNOWFLAKE_DATABASE")),
            "schema": org.get("schema", os.environ.get("SNOWFLAKE_SCHEMA")),
            "warehouse": org.get("warehouse", os.environ.get("SNOWFLAKE_WAREHOUSE")),
            "role": self._api_object.get("role", None) or f"{user}_role"
        }
