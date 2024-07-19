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
        opas = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'OP', id_permiso_ambiental__nombre__icontains = 'Inscripción del departamento de gestión ambiental (DGA)')

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
                    "Posee_Sistema_Gestion_Ambiental": "", # VALIDAR
                    "Posee_Sistema_Gestion": "", # VALIDAR
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
    
class GeoJsonInscripcionGeneradorRCDView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        opas = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'OP', id_permiso_ambiental__nombre__icontains = 'Inscripción como generador de residuos de construcción y demolición (RCD)')

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
                    "Nombre": opa.id_solicitud_tramite.nombre_proyecto,
                    "Latitud": opa.coordenada_x,
                    "Longitud": opa.coordenada_y,
                    "Area": "", # VALIDAR
                    "Fecha_Inicio_Obra": "", # VALIDAR
                    "Fecha_Estimada_Finalizacion": "", # VALIDAR
                    "Susceptibles_Aprovechamiento": "", # VALIDAR
                    "Susceptibles_No_Aprovechamiento": "", # VALIDAR
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
    
class GeoJsonInscripcionGeneradorACUView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        opas = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'OP', id_permiso_ambiental__nombre__icontains = 'Inscripción como generador de aceite de cocina usado (ACU)')

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
                    "Municipio": opa.cod_municipio.nombre,
                    "Tipo_Generador": "", # VALIDAR
                    "Cantidad_Generada": "", # VALIDAR
                    "Fecha_Inscripcion": opa.id_solicitud_tramite.fecha_registro.date(),
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
    
class GeoJsonInscripcionGestionACUView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        opas = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'OP', id_permiso_ambiental__nombre__icontains = 'Inscripción como gestor de aceite de cocina usado (ACU)')

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
                    "Municipio": opa.cod_municipio.nombre,
                    "Cantidad_Recoleccion_Realizada": "", # VALIDAR
                    "Cantidad_Almacenamiento_Realizado": "", # VALIDAR
                    "Cantidad_Aprovechamiento_Realizado": "", # VALIDAR
                    "Cantidad_Tratamiento_Realizado": "", # VALIDAR
                    "Fecha_Inscripcion": opa.id_solicitud_tramite.fecha_registro.date(),
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