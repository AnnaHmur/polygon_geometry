import sqlalchemy
from geoalchemy2 import Geometry

from datetime import datetime

from app.database import db, metadata

import pyproj

from shapely.ops import transform

pt = sqlalchemy.Table(
    "gis_polygon",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("class_id", sqlalchemy.Integer),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("props", sqlalchemy.JSON),
    sqlalchemy.Column("geom", Geometry("POLYGON")),
    sqlalchemy.Column("_created", sqlalchemy.TIMESTAMP),
    sqlalchemy.Column("_updated", sqlalchemy.TIMESTAMP),
)


class PolygonModel:
    DEFAULT_SRID = 4326
    
    @classmethod
    async def get(cls, polygon_id: int):
        query = pt.select().where(pt.c.id == polygon_id)
        polygon = await db.fetch_one(query)
        return polygon

    @classmethod
    async def create(cls, **polygon):
        query = pt.insert().values(**polygon, _created=datetime.now())
        polygon_id = await db.execute(query)
        return polygon_id

    @classmethod
    async def update(cls, polygon_id: int, **data):
        data["_updated"] = datetime.now()
        query = pt.update().where(pt.c.id == polygon_id).values(**data)
        await db.execute(query)

    @classmethod
    async def delete(cls, polygon_id: int):
        query = pt.delete().where(pt.c.id == polygon_id)
        _ = await db.execute(query)
