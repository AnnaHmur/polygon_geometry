import json
import pytest

from starlette.testclient import TestClient
from geoalchemy2 import WKBElement

from app.handlers import app
from app.models import PolygonModel


client = TestClient(app)

wkb_elem = WKBElement(
    data=b'\x01\x03\x00\x00 \xe6\x10\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00J@\x00\x00\x00'
         b'\x00\x00\x00\x08@fffff&J@\xe1z\x14\xaeG\xe1\x0c@fffff&J@\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00'
         b'\x00J@\x00\x00\x00\x00\x00\x00\x08@',
    srid=4326)

wkb_elem_updated = WKBElement(
    data=b'\x01\x03\x00\x00 \xe6\x10\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00J@\x00\x00\x00'
         b'\x00\x00\x00\x08@fffff&J@\xe1z\x14\xaeG\xe1\x0c@fffff&J@\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00'
         b'\x00J@\x00\x00\x00\x00\x00\x00\x08@',
    srid=32618
)

polygon_id = {
    'polygon_id': 1,
}

polygon = {
    'class_id': 0,
    'name': "test_polygon",
    'props': {},
    'geom': wkb_elem,
}


async def mock_create(**polygon):
    return 1


async def mock_get(_):
    return {
        **polygon_id,
        **polygon
}


async def mock_get_updated(_):
    return {
        **polygon_id,
        **polygon,
        "geom": wkb_elem_updated,
    }


async def mock_update(_, **polygon):
    return


async def mock_delete(_):
    return


def test_create_polygon__ok(monkeypatch):
    req_payload = {
        'class_id': 0,
        'name': "test_polygon",
        'props': {},
        'geom': 'POLYGON ((51.0 3.0, 51.3 3.61, 51.3 3.0, 51.0 3.0))',
        'srid': 4326,
    }

    resp_payload = polygon_id

    monkeypatch.setattr(PolygonModel, "create", mock_create)

    response = client.post("/api/v1/polygon/", json=req_payload,)
    assert response.status_code == 201
    assert response.json() == resp_payload


def test_create_polygon__invalid_payload(monkeypatch):
    req_payload = {
        'class_id': 0,
        'name': "test_polygon",
        'props': {},
        'geom': 'POLYGON ((51.0 3.0, 51.3 3.61, 51.3 3.0, 51.0 3.0))',
    }

    monkeypatch.setattr(PolygonModel, "create", mock_create)

    response = client.post("/api/v1/polygon/", json=req_payload,)
    assert response.status_code == 422


def test_create_polygon__invalid_srid(monkeypatch):
    req_payload = {
        'class_id': 0,
        'name': "test_polygon",
        'props': {},
        'geom': 'POLYGON ((51.0 3.0, 51.3 3.61, 51.3 3.0, 51.0 3.0))',
        'srid': 1000000000000,
    }

    monkeypatch.setattr(PolygonModel, "create", mock_create)

    response = client.post("/api/v1/polygon/", json=req_payload, )
    assert response.status_code == 422


def test_get_polygon__ok(monkeypatch):
    resp_payload = {
        "id": 1,
        "class_id": 0,
        "name": "test_polygon",
        "props": {},
        "geom": "POLYGON ((52 3, 52.3 3.61, 52.3 3, 52 3))"
    }

    monkeypatch.setattr(PolygonModel, "get", mock_get)

    response = client.get("/api/v1/polygon/1", params={'srid': 4326})
    assert response.status_code == 200
    assert response.json() == resp_payload


def test_get_polygon__ok_with_transform(monkeypatch):
    resp_payload = {
        "id": 1,
        "class_id": 0,
        "name": "test_polygon",
        "props": {},
        "geom": 'POLYGON ((7472781.60943401 19442551.04083275, 7409005.645953584 '
         '19335156.00979835, 7417523.935846412 19446413.45402157, '
         '7472781.60943401 19442551.04083275))'
    }

    monkeypatch.setattr(PolygonModel, "get", mock_get)

    response = client.get("/api/v1/polygon/1", params={'srid': 32618})
    assert response.status_code == 200
    assert response.json() == resp_payload


def test_get_polygon__invalid_srid(monkeypatch):
    monkeypatch.setattr(PolygonModel, "get", mock_get)

    response = client.get("/api/v1/polygon/1", params={'srid': 1000000000000})
    assert response.status_code == 422


def test_update_polygon__ok(monkeypatch):
    req_payload = {
        'class_id': 0,
        'name': "test_polygon",
        'props': {},
        'geom': "POLYGON ((52 3, 52.3 3.61, 52.3 3, 52 3))",
        'srid': 4326,
    }

    resp_payload = {
        "id": 1,
        "class_id": 0,
        "name": "test_polygon",
        "props": {},
        "geom": "POLYGON ((52 3, 52.3 3.61, 52.3 3, 52 3))"
    }

    monkeypatch.setattr(PolygonModel, "update", mock_update)
    monkeypatch.setattr(PolygonModel, "get", mock_get_updated)

    response = client.patch("/api/v1/polygon/1", json=req_payload)
    assert response.status_code == 200
    assert response.json() == resp_payload


def test_update_polygon__ok_with_transform(monkeypatch):
    req_payload = {
        'class_id': 0,
        'name': "test_polygon",
        'props': {},
        'geom': "POLYGON ((7472781.60943401 19442551.04083275, 7409005.645953584 19335156.00979835, 7417523.935846412 "
                "19446413.45402157, 7472781.60943401 19442551.04083275))",
        'srid': 32618,
    }

    resp_payload = {
        "id": 1,
        "class_id": 0,
        "name": "test_polygon",
        "props": {},
        "geom": "POLYGON ((7472781.60943401 19442551.04083275, 7409005.645953584 19335156.00979835, 7417523.935846412 "
                "19446413.45402157, 7472781.60943401 19442551.04083275))"
    }

    monkeypatch.setattr(PolygonModel, "update", mock_update)
    monkeypatch.setattr(PolygonModel, "get", mock_get_updated)

    response = client.patch("/api/v1/polygon/1", json=req_payload)
    assert response.status_code == 200
    assert response.json() == resp_payload


def test_update_polygon__invalid_srid(monkeypatch):
    req_payload = {
        'class_id': 0,
        'name': "test_polygon",
        'props': {},
        'geom': "POLYGON ((52 3, 52.3 3.61, 52.3 3, 52 3))",
        'srid': 1000000000000000000,
    }

    monkeypatch.setattr(PolygonModel, "update", mock_update)
    monkeypatch.setattr(PolygonModel, "get", mock_get_updated)

    response = client.patch("/api/v1/polygon/1", json=req_payload)
    assert response.status_code == 422


def test_delete_polygon__ok(monkeypatch):
    monkeypatch.setattr(PolygonModel, "delete", mock_delete)

    response = client.delete("/api/v1/polygon/1")
    assert response.status_code == 204
