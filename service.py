import pony.orm as pony
from models import db, Satellite, SpaceTrack
from starlink import datos
from math import cos, sin, sqrt


# Function that calculates the distance between two points given their longitudes, latitudes and heights
def distance_between_two_points(
    longitude_1, latitude_1, height_1, longitude_2, latitude_2, height_2
):
    return sqrt(
        (
            height_1 * cos(longitude_1 * 3.14 / 180) * sin(latitude_1 * 3.14 / 180)
            - height_2 * cos(longitude_2 * 3.14 / 180) * sin(latitude_2 * 3.14 / 180)
        )
        ** 2
        + (
            height_1 * sin(longitude_1 * 3.14 / 180) * sin(latitude_1 * 3.14 / 180)
            - height_2 * sin(longitude_2 * 3.14 / 180) * sin(latitude_2 * 3.14 / 180)
        )
        ** 2
        + (
            height_1 * cos(latitude_1 * 3.14 / 180)
            - height_2 * cos(latitude_2 * 3.14 / 180)
        )
        ** 2
    )


# Function that returns the list of all satellites
def list_all_satellites():
    with pony.db_session:
        satellites = db.Satellite.select()[:]
        return satellites


#
def list_satellites_whit_sub_name(name):
    with pony.db_session:
        satellites = db.Satellite.select().filter(
            lambda s: name in s.spaceTrack.OBJECT_NAME
        )[:]
        return satellites


# Function that returns the list of satellites that, given a latitude and longitude, are within a given radius
def list_satellites_in_radius_function(longitude, latitude, radius):
    if (
        longitude < -180
        or longitude > 180
        or latitude < -90
        or latitude > 90
        or radius < 0
    ):
        raise Exception("Invalid parameters")
    with pony.db_session:
        satellites_in_radius = []
        avg_height = pony.avg(s.height_km for s in db.Satellite)
        satellites = list_all_satellites()
        for s in satellites:
            if s.height_km != None and (
                distance_between_two_points(
                    s.longitude,
                    s.latitude,
                    s.height_km + 6378,
                    longitude,
                    latitude,
                    avg_height + 6378,
                )
                <= radius
            ):
                satellites_in_radius.append(s)
        return satellites_in_radius


# Function that creates a response model from a list of satellites for an endpoint
def create_response_model(satellites):
    response_model = []
    for s in satellites:
        r = {
            "spaceTrack": {
                "CCSDS_OMM_VERS": s.spaceTrack.CCSDS_OMM_VERS,
                "COMMENT": s.spaceTrack.COMMENT,
                "CREATION_DATE": s.spaceTrack.CREATION_DATE,
                "ORIGINATOR": s.spaceTrack.ORIGINATOR,
                "OBJECT_NAME": s.spaceTrack.OBJECT_NAME,
                "OBJECT_ID": s.spaceTrack.OBJECT_ID,
                "CENTER_NAME": s.spaceTrack.CENTER_NAME,
                "REF_FRAME": s.spaceTrack.REF_FRAME,
                "TIME_SYSTEM": s.spaceTrack.TIME_SYSTEM,
                "MEAN_ELEMENT_THEORY": s.spaceTrack.MEAN_ELEMENT_THEORY,
                "EPOCH": s.spaceTrack.EPOCH,
                "MEAN_MOTION": s.spaceTrack.MEAN_MOTION,
                "ECCENTRICITY": s.spaceTrack.ECCENTRICITY,
                "INCLINATION": s.spaceTrack.INCLINATION,
                "RA_OF_ASC_NODE": s.spaceTrack.RA_OF_ASC_NODE,
                "ARG_OF_PERICENTER": s.spaceTrack.ARG_OF_PERICENTER,
                "MEAN_ANOMALY": s.spaceTrack.MEAN_ANOMALY,
                "EPHEMERIS_TYPE": s.spaceTrack.EPHEMERIS_TYPE,
                "CLASSIFICATION_TYPE": s.spaceTrack.CLASSIFICATION_TYPE,
                "NORAD_CAT_ID": s.spaceTrack.NORAD_CAT_ID,
                "ELEMENT_SET_NO": s.spaceTrack.ELEMENT_SET_NO,
                "REV_AT_EPOCH": s.spaceTrack.REV_AT_EPOCH,
                "BSTAR": s.spaceTrack.BSTAR,
                "MEAN_MOTION_DOT": s.spaceTrack.MEAN_MOTION_DOT,
                "MEAN_MOTION_DDOT": s.spaceTrack.MEAN_MOTION_DDOT,
                "SEMIMAJOR_AXIS": s.spaceTrack.SEMIMAJOR_AXIS,
                "PERIOD": s.spaceTrack.PERIOD,
                "APOAPSIS": s.spaceTrack.APOAPSIS,
                "PERIAPSIS": s.spaceTrack.PERIAPSIS,
                "OBJECT_TYPE": s.spaceTrack.OBJECT_TYPE,
                "RCS_SIZE": s.spaceTrack.RCS_SIZE,
                "COUNTRY_CODE": s.spaceTrack.COUNTRY_CODE,
                "LAUNCH_DATE": s.spaceTrack.LAUNCH_DATE,
                "SITE": s.spaceTrack.SITE,
                "DECAY_DATE": s.spaceTrack.DECAY_DATE,
                "DECAYED": s.spaceTrack.DECAYED,
                "FILE": s.spaceTrack.FILE,
                "GP_ID": s.spaceTrack.GP_ID,
                "TLE_LINE0": s.spaceTrack.TLE_LINE0,
                "TLE_LINE1": s.spaceTrack.TLE_LINE1,
                "TLE_LINE2": s.spaceTrack.TLE_LINE2,
            },
            "launch": s.launch,
            "version": s.version,
            "height_km": s.height_km,
            "latitude": s.latitude,
            "longitude": s.longitude,
            "velocity_kms": s.velocity_kms,
            "id": s.id,
        }
        response_model.append(r)
    return response_model


# Function to load data and perform tests
@pony.db_session()
def data_loading():
    for i in range(0, len(datos)):
        sT = SpaceTrack(
            CCSDS_OMM_VERS=datos[i]["spaceTrack"]["CCSDS_OMM_VERS"],
            COMMENT=datos[i]["spaceTrack"]["COMMENT"],
            CREATION_DATE=datos[i]["spaceTrack"]["CREATION_DATE"],
            ORIGINATOR=datos[i]["spaceTrack"]["ORIGINATOR"],
            OBJECT_NAME=datos[i]["spaceTrack"]["OBJECT_NAME"],
            OBJECT_ID=datos[i]["spaceTrack"]["OBJECT_ID"],
            CENTER_NAME=datos[i]["spaceTrack"]["CENTER_NAME"],
            REF_FRAME=datos[i]["spaceTrack"]["REF_FRAME"],
            TIME_SYSTEM=datos[i]["spaceTrack"]["TIME_SYSTEM"],
            MEAN_ELEMENT_THEORY=datos[i]["spaceTrack"]["MEAN_ELEMENT_THEORY"],
            EPOCH=datos[i]["spaceTrack"]["EPOCH"],
            MEAN_MOTION=datos[i]["spaceTrack"]["MEAN_MOTION"],
            ECCENTRICITY=datos[i]["spaceTrack"]["ECCENTRICITY"],
            INCLINATION=datos[i]["spaceTrack"]["INCLINATION"],
            RA_OF_ASC_NODE=datos[i]["spaceTrack"]["RA_OF_ASC_NODE"],
            ARG_OF_PERICENTER=datos[i]["spaceTrack"]["ARG_OF_PERICENTER"],
            MEAN_ANOMALY=datos[i]["spaceTrack"]["MEAN_ANOMALY"],
            EPHEMERIS_TYPE=datos[i]["spaceTrack"]["EPHEMERIS_TYPE"],
            CLASSIFICATION_TYPE=datos[i]["spaceTrack"]["CLASSIFICATION_TYPE"],
            NORAD_CAT_ID=datos[i]["spaceTrack"]["NORAD_CAT_ID"],
            ELEMENT_SET_NO=datos[i]["spaceTrack"]["ELEMENT_SET_NO"],
            REV_AT_EPOCH=datos[i]["spaceTrack"]["REV_AT_EPOCH"],
            BSTAR=datos[i]["spaceTrack"]["BSTAR"],
            MEAN_MOTION_DOT=datos[i]["spaceTrack"]["MEAN_MOTION_DOT"],
            MEAN_MOTION_DDOT=datos[i]["spaceTrack"]["MEAN_MOTION_DDOT"],
            SEMIMAJOR_AXIS=datos[i]["spaceTrack"]["SEMIMAJOR_AXIS"],
            PERIOD=datos[i]["spaceTrack"]["PERIOD"],
            APOAPSIS=datos[i]["spaceTrack"]["APOAPSIS"],
            PERIAPSIS=datos[i]["spaceTrack"]["PERIAPSIS"],
            OBJECT_TYPE=datos[i]["spaceTrack"]["OBJECT_TYPE"],
            RCS_SIZE=datos[i]["spaceTrack"]["RCS_SIZE"],
            COUNTRY_CODE=datos[i]["spaceTrack"]["COUNTRY_CODE"],
            LAUNCH_DATE=datos[i]["spaceTrack"]["LAUNCH_DATE"],
            SITE=datos[i]["spaceTrack"]["SITE"],
            DECAY_DATE=datos[i]["spaceTrack"]["DECAY_DATE"],
            DECAYED=datos[i]["spaceTrack"]["DECAYED"],
            FILE=datos[i]["spaceTrack"]["FILE"],
            GP_ID=datos[i]["spaceTrack"]["GP_ID"],
            TLE_LINE0=datos[i]["spaceTrack"]["TLE_LINE0"],
            TLE_LINE1=datos[i]["spaceTrack"]["TLE_LINE1"],
            TLE_LINE2=datos[i]["spaceTrack"]["TLE_LINE2"],
        )
        pony.commit()
        s = Satellite(
            spaceTrack=sT,
            launch=datos[i]["launch"],
            version=datos[i]["version"],
            height_km=datos[i]["height_km"],
            latitude=datos[i]["latitude"],
            longitude=datos[i]["longitude"],
            velocity_kms=datos[i]["velocity_kms"],
            id=datos[i]["id"],
        )
        pony.commit()
        sT.satellite = s
        pony.commit()
