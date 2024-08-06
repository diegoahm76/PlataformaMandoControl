from datetime import date
from django.db.models import Q
import os
import arcgis
from geojson.lists.geojsons_list import geojsons_LIST

def update_arcgis_layers():
    # AUTENTICAR CON ARCGIS
    profile = os.environ.get('PROFILE_ARCGIS')
    username = os.environ.get('USERNAME_ARCGIS')
    password = os.environ.get('PASSWORD_ARCGIS')

    arcgis.GIS(profile=profile, username=username, password=password)

    # ACTUALIZAR GEOJSONS
    backend_host = "https://bia.cormacarena.gov.co/apimando/geojson"

    for geojson in geojsons_LIST:
        geojson_url = f"{backend_host}{geojson['url']}"
        os.system(f"python ./scripts/OverwriteFS.py {profile} {geojson['id']} {geojson['title']} {geojson_url}")