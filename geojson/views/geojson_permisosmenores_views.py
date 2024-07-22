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
    
class GeoJsonPermisoCazaView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        permisos_menores = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PM', id_permiso_ambiental__nombre__icontains = 'Permiso de caza de fauna silvestre')

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
                    "OBJECTID": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                    "Municipio": permiso_menor.cod_municipio.nombre,
                    "Fecha": permiso_menor.id_solicitud_tramite.fecha_registro.date(),
                    "Usuario": permiso_menor.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Numero_Expediente": UtilsGeoJson.get_expediente(permiso_menor),
                    "Latitud": permiso_menor.coordenada_x,
                    "Longitud": permiso_menor.coordenada_y,
                    "Termino_Permiso_Vigencia": "", # VALIDAR
                    "Numero_Resolucion": "", # VALIDAR
                    "Fecha_Inicio_Vigencia": "", # VALIDAR
                    "Fecha_Fin_Vigencia": "" # VALIDAR
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
    
class GeoJsonRedAmigosSilvestresView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        permisos_menores = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PM', id_permiso_ambiental__nombre__icontains = 'Licencia de red de amigos de la fauna silvestre')

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
                    "OBJECTID": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                    "Usuario": permiso_menor.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Municipio": permiso_menor.cod_municipio.nombre,
                    "Latitud": permiso_menor.coordenada_x,
                    "Longitud": permiso_menor.coordenada_y,
                    "Numero_Expediente": UtilsGeoJson.get_expediente(permiso_menor),
                    "Tipo_Licencia_Funcionamiento": "", # VALIDAR
                    "Termino_Licencia": "", # VALIDAR
                    "Numero_Resolucion_Funcionamiento_Temporal": "", # VALIDAR
                    "Resolucion_Funcionamiento_Definitivo": "" # VALIDAR
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
    

class GeoJsonRegistroPlantacionesForestales(generics.ListAPIView):

    def get(self, request):
        permisos_menores = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PM', id_permiso_ambiental__nombre__icontains = 'Registro de plantaciones forestales protectoras y/o protectoras-productoras')

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
                    "OBJECTID": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                    "Nombre": "", # VALIDAR
                    "Numero_Matricula": "", # VALIDAR
                    "Numero_Codigo":"", # VALIDAR
                    "Latitud": permiso_menor.coordenada_x,
                    "Longitud": permiso_menor.coordenada_y, 
                    "Altura": "", # VALIDAR
                    "Municipio" :permiso_menor.cod_municipio.nombre,
                    "Uso_Suelo_POT":"", # VALIDAR
                    "Usuario": permiso_menor.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Resolucion": "", # VALIDAR
                    "Fecha_Expedicion" :"", # VALIDAR
                    "Expedicion": "", # VALIDAR
                    "Vigencia":"", # VALIDAR
                    "Fecha_Expedicion_Resolucion": "", # VALIDAR
                    "Fecha_Exacta_Inicio_Vigencia": "" # VALIDAR
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
    

class GeoJsonRegistroLicenciaZoocriadero(generics.ListAPIView):

    def get(self, request):
        permisos_menores = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PM', id_permiso_ambiental__nombre__icontains = 'Licencia de establecimiento de zoocriadero de fauna silvestre')

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
                    "OBJECTID": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                    "Nombre": "", # VALIDAR
                    "Usuario": permiso_menor.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Tematica_Zoocriadero":"", # VALIDAR
                    "Municipio" :permiso_menor.cod_municipio.nombre,
                    "Expediente": UtilsGeoJson.get_expediente(permiso_menor),
                    "Tipo_Licencia_Ambiental": "", # VALIDAR
                    "Fecha_Inicio_Vigencia": "", # VALIDAR
                    "Fecha_Fin_Vigencia": "" # VALIDAR
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


class GeoJsonPermisoZoologico(generics.ListAPIView):

    def get(self, request):
        permisos_menores = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PM', id_permiso_ambiental__nombre__icontains = 'Permiso ambiental para funcionamiento de zoológicos')

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
                    "OBJECTID": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                    "Municipio" :permiso_menor.cod_municipio.nombre,
                    "Usuario": permiso_menor.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Latitud": permiso_menor.coordenada_x,
                    "Longitud": permiso_menor.coordenada_y,
                    "Tematica_Zoologico":"", # VALIDAR
                    "Numero_Expediente": UtilsGeoJson.get_expediente(permiso_menor),
                    "Tipo_Licencia_Funcionamiento": "", # VALIDAR
                    "Termino_Licencia": "", # VALIDAR
                    "Fecha_Inicio_Vigencia": "", # VALIDAR
                    "Fecha_Fin_Vigencia": "", # VALIDAR
                    "Resolucion_Funcionamiento_Temporal": "", # VALIDAR
                    "Resolucion_Funcionamiento_Definitivo": "" # VALIDAR
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

