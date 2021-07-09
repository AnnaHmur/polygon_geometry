import pyproj
from pyproj.crs import CRSError

from geoalchemy2 import WKBElement
from shapely.errors import WKTReadingError
from shapely.wkt import loads
from pydantic import BaseModel, Field, validator


class SRIDField(int):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate


    @classmethod
    def validate(cls, value):
        if not isinstance(value, int):
            value = int(value)

        epsg = f'EPSG:{value}'
        try:
            _ = pyproj.CRS(epsg)
        except CRSError:
            raise ValueError(f'Unknown EPSG value: {epsg}')

        return value


class PolygonSchema(BaseModel):
    class_id: int
    name: str
    props: dict
    geom: str = Field(description="Example: \"POLYGON ((51.0 3.0, 51.3 3.61, 51.3 3.0, 51.0 3.0))\"")
    srid: SRIDField

    class Config:
        orm_mode = True
        
    @validator("geom")
    def validate_geom(cls, value):
        try:
            _ = loads(value)
        except WKTReadingError:
            raise ValueError(" Could not parse `geom` parameter because of invalid input")
        
        return value


class PolygonResponseSchema(BaseModel):
    id: int
    class_id: int
    name: str
    props: dict
    geom: str

