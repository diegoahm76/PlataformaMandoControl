
import requests
import json
import os
from geojson.functions.alertas import  update_arcgis_layers
from datetime import datetime, timedelta
# from recaudo.Extraccion.ExtraccionBaseDatosPimisis import  extraccion_pimisis_job  # Importa la función ExtraccionBaseDatosPimisis


def update_arcgis():
	update_arcgis_layers()
	print('FINISH CRONJOB')