import json
from rest_framework.exceptions import ValidationError,NotFound,PermissionDenied
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from geojson.utils import UtilsGeoJson
from geojson.models.tramites_models import PermisosAmbSolicitudesTramite
    
class GeoJsonInscripcionDGAView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        opas = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'OP', id_permiso_ambiental__nombre__icontains = 'DGA')

        GeoJson_list = []

        for opa in opas:

            GeoJson = {
                "type": "Feature",
                "id": opa.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [opa.coordenada_x, opa.coordenada_y]
                },
                "properties": {
                    "OBJECTID": opa.id_solicitud_tramite.id_solicitud_tramite,
                    "Usuario": opa.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Tipo_DGA": opa.id_solicitud_tramite.get_cod_tipo_operacion_tramite_display(),
                    "Persona_Encargada": UtilsGeoJson.get_nombre_persona(opa.id_solicitud_tramite.id_persona_titular),
                    "Telefono_Contacto": opa.id_solicitud_tramite.id_persona_titular.telefono_celular,
                    "Correo_Contacto": opa.id_solicitud_tramite.id_persona_titular.email,
                    "Posee_Sistema_Gestion_Ambiental": "SI", # VALIDAR
                    "Posee_Sistema_Gestion": "SI", # VALIDAR
                    "Fecha_Inscripcion": opa.id_solicitud_tramite.fecha_registro.date(),
                    "Municipio": opa.cod_municipio.nombre
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
    

class GeoJsonFormulacionProyectosEscolaresView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        opas = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'OP', id_permiso_ambiental__nombre__icontains = 'Apoyo formulación e implementación de proyectos ambientales escolares')

        GeoJson_list = []

        for opa in opas:

            GeoJson = {
                "type": "Feature",
                "id": opa.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [opa.coordenada_x, opa.coordenada_y]
                },
                "properties": {
                    "OBJECTID": opa.id_solicitud_tramite.id_solicitud_tramite,
                    "Municipio": opa.cod_municipio.nombre,
                    "Nombre_Colegio": "Validar", # VALIDAR
                    "Nombre_PRAE": "Validar", # VALIDAR
                    "latitud": opa.coordenada_x,
                    "longitud": opa.coordenada_y,
                    "Persona_Encargado": UtilsGeoJson.get_nombre_persona(opa.id_solicitud_tramite.id_persona_titular),
                    "Actividades_Realizadas": "Validar", # VALIDAR
                    "Fecha_Inscripcion": opa.id_solicitud_tramite.fecha_registro.date(),
                }
            }
            GeoJson_list.append(GeoJson)

        return Response(GeoJson_list)