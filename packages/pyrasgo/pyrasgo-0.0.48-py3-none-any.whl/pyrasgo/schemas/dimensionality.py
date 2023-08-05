from pydantic import BaseModel

from pyrasgo.schemas.organization import Organization


class Dimensionality(BaseModel):
    id: int


class DimensionalityCreate(BaseModel):
    name: str
    dimension_type: str
    granularity: str
    organization: Organization
