from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from shapely.wkt import loads
from geoalchemy2.shape import to_shape

from app.database import db
from app.models import PolygonModel
from app.schemas import PolygonSchema, PolygonResponseSchema, SRIDField
from app.helpers import transform_polygon


app = FastAPI()


@app.post("/api/v1/polygon/", status_code=status.HTTP_201_CREATED)
async def create_polygon(polygon: PolygonSchema):
    geom = loads(polygon.geom)
    
    polygon.geom = str(transform_polygon(geom, srid_from=polygon.srid, srid_to=PolygonModel.DEFAULT_SRID))

    p = polygon.dict()
    p.pop("srid")

    polygon_id = await PolygonModel.create(**p)
    return {
        "polygon_id": polygon_id,
    }


@app.get("/api/v1/polygon/{polygon_id}", response_model=PolygonResponseSchema)
async def get_polygon(polygon_id: int, srid: SRIDField):
    polygon = await PolygonModel.get(polygon_id)
    geom = to_shape(polygon["geom"])

    return PolygonResponseSchema(
        id=polygon_id,
        name=polygon["name"],
        class_id=polygon["class_id"],
        props=polygon["props"],
        geom=str(transform_polygon(geom, srid_from=PolygonModel.DEFAULT_SRID, srid_to=srid))
    ).dict()


@app.patch("/api/v1/polygon/{polygon_id}", response_model=PolygonResponseSchema)
async def update_polygon(polygon_id: int, polygon: PolygonSchema):
    geom = loads(polygon.geom)
    
    polygon.geom = str(transform_polygon(geom, srid_from=polygon.srid, srid_to=PolygonModel.DEFAULT_SRID))
    
    p = polygon.dict()
    srid = p.pop("srid")
    
    await PolygonModel.update(polygon_id, **p)
    polygon = await PolygonModel.get(polygon_id)

    geom = to_shape(polygon["geom"])
    return PolygonResponseSchema(
        id=polygon_id,
        name=polygon["name"],
        class_id=polygon["class_id"],
        props=polygon["props"],
        geom=str(transform_polygon(geom, srid_from=PolygonModel.DEFAULT_SRID, srid_to=srid)),
    ).dict()


@app.delete("/api/v1/polygon/{polygon_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_polygon(polygon_id: int):
    await PolygonModel.delete(polygon_id)
    return {}


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
