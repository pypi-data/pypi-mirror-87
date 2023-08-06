import csv
import io

from aiohttp import ClientSession
from dateutil.parser import isoparse
from geopy import distance

SITE_LIST_URL = "https://dd.weather.gc.ca/hydrometric/doc/hydrometric_StationList.csv"
READINGS_URL = "https://dd.weather.gc.ca/hydrometric/csv/{prov}/hourly/{prov}_{station}_hourly_hydrometric.csv"


async def get_hydro_sites():
    """Get list of all sites from Environment Canada, for auto-config."""

    sites = []

    async with ClientSession() as session:
        response = await session.get(SITE_LIST_URL, timeout=10)
        result = await response.read()
    sites_csv_string = result.decode("utf-8-sig")
    sites_csv_stream = io.StringIO(sites_csv_string)

    header = [h.split("/")[0].strip() for h in sites_csv_stream.readline().split(",")]
    sites_reader = csv.DictReader(sites_csv_stream, fieldnames=header)

    for site in sites_reader:
        site["Latitude"] = float(site["Latitude"])
        site["Longitude"] = float(site["Longitude"])
        sites.append(site)

    return sites


async def closest_site(lat, lon):
    """Return the province/site_code of the closest station to our lat/lon."""
    site_list = await get_hydro_sites()

    def site_distance(site):
        """Calculate distance to a site."""
        return distance.distance((lat, lon), (site["Latitude"], site["Longitude"]))

    closest = min(site_list, key=site_distance)

    return closest


class ECHydro(object):

    """Get hydrometric data from Environment Canada."""

    def __init__(self, province=None, station=None, coordinates=None):
        """Initialize the data object."""
        self.measurements = {}
        self.timestamp = None
        self.location = None

        if province and station:
            self.province = province
            self.station = station
        elif coordinates:
            self.province = None
            self.station = None
            self.coordinates = coordinates

    async def update(self):
        """Get the latest data from Environment Canada."""

        # Determine closest site if not provided

        if not (self.province and self.station) and self.coordinates:
            closest = await closest_site(*self.coordinates)
            self.province = closest["Prov"]
            self.station = closest["ID"]
            self.location = closest["Name"].title()

        # Get hydrometric data

        async with ClientSession() as session:
            response = await session.get(
                READINGS_URL.format(prov=self.province, station=self.station),
                timeout=10,
            )
            result = await response.read()
        hydro_csv_string = result.decode("utf-8-sig")
        hydro_csv_stream = io.StringIO(hydro_csv_string)

        header = [
            h.split("/")[0].strip() for h in hydro_csv_stream.readline().split(",")
        ]
        readings_reader = csv.DictReader(hydro_csv_stream, fieldnames=header)

        readings = [r for r in readings_reader]
        if len(readings) > 0:
            latest = readings[-1]

            if latest["Water Level"] != "":
                self.measurements["water_level"] = {
                    "label": "Water Level",
                    "value": float(latest["Water Level"]),
                    "unit": "m",
                }

            if latest["Discharge"] != "":
                self.measurements["discharge"] = {
                    "label": "Discharge",
                    "value": float(latest["Discharge"]),
                    "unit": "m³/s",
                }

            self.timestamp = isoparse(readings[-1]["Date"])
