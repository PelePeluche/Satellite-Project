from fastapi import FastAPI, status, HTTPException
import pony.orm as pony
from typing import Optional


from service import (
    list_satellites_in_radius_function,
    create_response_model,
    list_all_satellites,
    list_satellites_whit_sub_name,
)


description = """
### 🚀 **Satellite coordination system that allows scientists to analyze the positions of active satellites** 🚀

## Endpoints implemented

### GET /starlink
Returns the list of all satellites. In addition, you can enter a "string" so that the method returns the list of satellites whose name contains this "string".

### GET /starlink/satellites-in-radius
It takes as parameters a *latitude*, *longitude* and *radius*. This endpoint generates a point in space whose *longitude* and *latitude* are those entered as parameters and whose height is the average height of all the satellites in the database added to the radius of the Earth (*6378 km*). In this way, all satellites whose distance to this generated point is less than or equal to the *radius* entered as parameter are returned.

"""

app = FastAPI(
    title="Satellite coordination system DOCS",
    description=description,
)

# Endpoint returning the list of all satellites
@app.get("/starlink")
async def list_satellites_endpoint(name: Optional[str] = None):
    with pony.db_session:
        if name == None:
            satellites = list_all_satellites()
        else:
            satellites = list_satellites_whit_sub_name(name)
        response = create_response_model(satellites)
        return response


# Endpoint that returns the list of all satellites that satisfy that given a point (latitude and longitude) are at a distance less than or equal to a given radius.
@app.get("/starlink/satellites-in-radius")
async def list_satellites_in_radius_endpoint(
    latitude: float, longitude: float, radius: float
):
    if latitude > 90 or latitude < -90:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid latitude"
        )
    if longitude > 180 or longitude < -180:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid longitude"
        )
    if radius < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid radius"
        )
    with pony.db_session:
        satellites_in_radius = list_satellites_in_radius_function(
            longitude, latitude, radius
        )
        response = create_response_model(satellites_in_radius)
        return response
