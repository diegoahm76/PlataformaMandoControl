import json
from seguridad.utils import Util
from rest_framework.exceptions import ValidationError,NotFound,PermissionDenied
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from geojson.utils import UtilsGeoJson
from geojson.models.tramites_models import SolicitudesTramites, PermisosAmbientales, PermisosAmbSolicitudesTramite
from geojson.models.estaciones_models import Estaciones



class GeoJsonEstacionesView(generics.ListAPIView):
    def get(self, request):
        estaciones = Estaciones.objects.all()

        GeoJson_list = []

        for estacion in estaciones:
            GeoJson = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(estacion.longitud), float(estacion.latitud)]
                },
                "properties": {
                    "id_estacion": estacion.id_estacion,
                    "nombre_estacion": estacion.nombre_estacion,
                    "cod_tipo_estacion": estacion.cod_tipo_estacion,
                    "cod_municipio": estacion.cod_municipio,
                    "indicaciones_ubicacion": estacion.indicaciones_ubicacion,
                    "fecha_modificacion": estacion.fecha_modificacion,
                    "fecha_modificacion_coordenadas": estacion.fecha_modificacion_coordenadas,
                    "id_persona_modifica": estacion.id_persona_modifica,
                }
            }
            GeoJson_list.append(GeoJson)

        return Response({
            "type": "FeatureCollection",
            "features": GeoJson_list
        })
