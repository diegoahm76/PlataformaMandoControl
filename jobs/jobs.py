from geojson.functions.alertas import update_arcgis_tramites_layers, update_arcgis_estaciones_layers

def update_tramites_arcgis():
	update_arcgis_tramites_layers()
	print('FINISH CRONJOB TRAMITES')


def update_estaciones_arcgis():
	update_arcgis_estaciones_layers()
	print('FINISH CRONJOB ESTACIONES')