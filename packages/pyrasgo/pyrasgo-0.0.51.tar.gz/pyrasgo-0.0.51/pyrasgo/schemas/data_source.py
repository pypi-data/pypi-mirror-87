from pydantic import BaseModel
from typing import Optional

from pyrasgo.schemas.organization import Organization


class DataSourceBase(BaseModel):
    id: int


class DataSourceCreate(BaseModel):
    name: str
    abbreviation: str
    organization: Organization


class DataSource(DataSourceBase):
    name: Optional[str]  # TODO: Should not be optional
    category: Optional[str] = None
