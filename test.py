from fastapi.testclient import TestClient
import pony.orm as pony
from main import app
from models import db
from fastapi import status

from service import (
    list_all_satellites,
    list_satellites_whit_sub_name,
    list_satellites_in_radius_function,
)


client = TestClient(app)


@pony.db_session
def test_list_all_satellites_len():
    satellites = list_all_satellites()
    satellites_from_db_count = pony.count(s for s in db.Satellite)

    assert len(satellites) == satellites_from_db_count


@pony.db_session
def test_list_satellites_filter_by_subname():
    satellites = list_satellites_whit_sub_name("200")
    for s in satellites:
        assert "200" in s.spaceTrack.OBJECT_NAME


@pony.db_session
def test_list_satellites_filter_by_subname_ridiculus():
    satellites = list_satellites_whit_sub_name("ásñdlpo123'09asdpàod`pasd")
    assert len(satellites) == 0


@pony.db_session
def test_list_satellites_in_big_radius():
    satellites = list_satellites_in_radius_function(0, 0, 1000000)
    satellites_from_db_count = pony.count(
        s for s in db.Satellite if s.height_km != None
    )
    assert len(satellites) == satellites_from_db_count


@pony.db_session
def test_list_satellites_in_medium_radius():
    satellites = list_satellites_in_radius_function(0, 0, 1000)
    satellites_from_db_count = pony.count(
        s for s in db.Satellite if s.height_km != None
    )
    assert len(satellites) <= satellites_from_db_count


@pony.db_session
def test_list_satellites_endpoint_without_name():
    response = client.get("/starlink")
    assert response.status_code == status.HTTP_200_OK


@pony.db_session
def test_list_satellites_endpoint_with_name():
    response = client.get("/starlink?name=2634")
    assert response.status_code == status.HTTP_200_OK


@pony.db_session
def test_list_satellites_in_radius_endpoint():
    response = client.get(
        "/starlink/satellites-in-radius?latitude=0&longitude=0&radius=100"
    )
    assert response.status_code == status.HTTP_200_OK


@pony.db_session
def test_list_satellites_in_radius_endpoint_invalid_latitude():
    response = client.get(
        "/starlink/satellites-in-radius?latitude=-200&longitude=0&radius=100"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pony.db_session
def test_list_satellites_in_radius_endpoint_invalid_longitud():
    response = client.get(
        "/starlink/satellites-in-radius?latitude=-20&longitude=1000&radius=100"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pony.db_session
def test_list_satellites_in_radius_endpoint_invalid_radius():
    response = client.get(
        "/starlink/satellites-in-radius?latitude=-20&longitude=0&radius=-1"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
