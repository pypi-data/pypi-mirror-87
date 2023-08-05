from typing import Optional
from pydantic import BaseModel
from pyrasgo.schemas.dimensionality import Dimensionality
from pyrasgo.schemas.feature_set import v0


class ColumnCreate(BaseModel):
    name: str
    dataType: str
    featureSet: v0.FeatureSetBase
    dimensionality: Dimensionality


class ColumnUpdate(BaseModel):
    id: int
    name: Optional[str]
    dataType: Optional[str]
    featureSet: Optional[v0.FeatureSetBase]
    dimensionality: Optional[Dimensionality]


class Column(BaseModel):
    id: Optional[int]
