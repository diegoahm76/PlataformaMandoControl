import json
from rest_framework.exceptions import ValidationError,NotFound,PermissionDenied
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from geojson.utils import UtilsGeoJson
from geojson.models.tramites_models import PermisosAmbSolicitudesTramite
    
class GeoJsonCertificacionInscripcionControlView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        permisos_menores = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PM', id_permiso_ambiental__nombre__icontains = 'Certificación de las inversiones de control, conservación y mejoramiento del medio ambiente')

        GeoJson_list = []

        for permiso_menor in permisos_menores:

            GeoJson = {
                "type": "Feature",
                "id": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [permiso_menor.coordenada_x, permiso_menor.coordenada_y]
                },
                "properties": {
                    "Usuario": UtilsGeoJson.get_nombre_persona(permiso_menor.id_solicitud_tramite.id_persona_titular),
                    "latitud": permiso_menor.coordenada_x,
                    "longitud": permiso_menor.coordenada_y,
                    "resolucion": permiso_menor.id_permiso_ambiental.resolucion, #Validar
                    "expediente": UtilsGeoJson.get_expediente(permiso_menor),
                    "vigencia": permiso_menor.id_permiso_ambiental.vigencia, #Validar
                    "fecha_expedicion_resolucion": permiso_menor.id_permiso_ambiental.fecha_expedicion, #Validar
                    "fecha_exacta_inicio_vigencia": permiso_menor.id_permiso_ambiental.fecha_inicio_vigencia, #Validar
                }
            }
            GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:4326" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    