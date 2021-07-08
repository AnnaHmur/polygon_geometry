import pyproj

from shapely.geometry import Polygon
from shapely.ops import transform


def transform_polygon(polygon: Polygon, srid_from: int, srid_to: int) -> Polygon:
    if srid_from == srid_to:
        return polygon

    from_ = pyproj.CRS(f"EPSG:{srid_from}")
    to_ = pyproj.CRS(f"EPSG:{srid_to}")

    pjt = pyproj.Transformer.from_crs(from_, to_, always_xy=True).transform
    transformed = transform(pjt, polygon)
    
    return transformed
