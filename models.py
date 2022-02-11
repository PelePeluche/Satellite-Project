import pony.orm as pony


db = pony.Database()


class Satellite(db.Entity):
    spaceTrack = pony.Required("SpaceTrack", reverse="satellite")
    launch = pony.Optional(str, nullable=True)
    version = pony.Optional(str, nullable=True)
    height_km = pony.Optional(float)
    latitude = pony.Optional(float)
    longitude = pony.Optional(float)
    velocity_kms = pony.Optional(float)
    id = pony.PrimaryKey(str)


class SpaceTrack(db.Entity):
    satellite = pony.Optional("Satellite", reverse="spaceTrack")
    CCSDS_OMM_VERS = pony.Optional(str, nullable=True)
    COMMENT = pony.Optional(str, nullable=True)
    CREATION_DATE = pony.Optional(str, nullable=True)
    ORIGINATOR = pony.Optional(str, nullable=True)
    OBJECT_NAME = pony.Required(str, nullable=True)
    OBJECT_ID = pony.PrimaryKey(str)
    CENTER_NAME = pony.Optional(str, nullable=True)
    REF_FRAME = pony.Optional(str, nullable=True)
    TIME_SYSTEM = pony.Optional(str, nullable=True)
    MEAN_ELEMENT_THEORY = pony.Optional(str, nullable=True)
    EPOCH = pony.Optional(str, nullable=True)
    MEAN_MOTION = pony.Optional(float)
    ECCENTRICITY = pony.Optional(float)
    INCLINATION = pony.Optional(float)
    RA_OF_ASC_NODE = pony.Optional(float)
    ARG_OF_PERICENTER = pony.Optional(float)
    MEAN_ANOMALY = pony.Optional(float)
    EPHEMERIS_TYPE = pony.Optional(int)
    CLASSIFICATION_TYPE = pony.Optional(str, nullable=True)
    NORAD_CAT_ID = pony.Optional(int)
    ELEMENT_SET_NO = pony.Optional(int)
    REV_AT_EPOCH = pony.Optional(int)
    BSTAR = pony.Optional(float)
    MEAN_MOTION_DOT = pony.Optional(float)
    MEAN_MOTION_DDOT = pony.Optional(float)
    SEMIMAJOR_AXIS = pony.Optional(float)
    PERIOD = pony.Optional(float)
    APOAPSIS = pony.Optional(float)
    PERIAPSIS = pony.Optional(float)
    OBJECT_TYPE = pony.Optional(str, nullable=True)
    RCS_SIZE = pony.Optional(str, nullable=True)
    COUNTRY_CODE = pony.Optional(str, nullable=True)
    LAUNCH_DATE = pony.Optional(str, nullable=True)
    SITE = pony.Optional(str, nullable=True)
    DECAY_DATE = pony.Optional(str, nullable=True)
    DECAYED = pony.Optional(int)
    FILE = pony.Optional(int)
    GP_ID = pony.Optional(int)
    TLE_LINE0 = pony.Optional(str, nullable=True)
    TLE_LINE1 = pony.Optional(str, nullable=True)
    TLE_LINE2 = pony.Optional(str, nullable=True)


# Line used for debugging
pony.set_sql_debug(True)

# Creation of tables for the models
db.bind("sqlite", "database.sqlite", create_db=True)
db.generate_mapping(create_tables=True)
