import json
from rest_framework.exceptions import ValidationError,NotFound,PermissionDenied
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from geojson.utils import UtilsGeoJson
from geojson.models.tramites_models import PermisosAmbSolicitudesTramite, Predios
    
class GeoJsonCertificacionInscripcionControlView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        permisos_menores = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PM', id_permiso_ambiental__nombre__icontains = 'Certificación de las inversiones de control, conservación y mejoramiento del medio ambiente')

        GeoJson_list = []

        for permiso_menor in permisos_menores:
            lat, lon = UtilsGeoJson.get_coordinates(permiso_menor.coordenada_x, permiso_menor.coordenada_y)

            GeoJson = {
                "type": "Feature",
                "id": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "Usuario": UtilsGeoJson.get_nombre_persona(permiso_menor.id_solicitud_tramite.id_persona_titular),
                    "latitud": lat,
                    "longitud": lon,
                    "resolucion": "", #Validar
                    "expediente": UtilsGeoJson.get_expediente(permiso_menor),
                    "vigencia": "", #Validar
                    "fecha_expedicion_resolucion": "", #Validar
                    "fecha_exacta_inicio_vigencia": "", #Validar
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
            lat, lon = UtilsGeoJson.get_coordinates(permiso_menor.coordenada_x, permiso_menor.coordenada_y)

            GeoJson = {
                "type": "Feature",
                "id": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "OBJECTID": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                    "Municipio": permiso_menor.cod_municipio.nombre,
                    "Fecha": permiso_menor.id_solicitud_tramite.fecha_registro.date(),
                    "Usuario": permiso_menor.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Numero_Expediente": UtilsGeoJson.get_expediente(permiso_menor),
                    "Latitud": lat,
                    "Longitud": lon,
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
            lat, lon = UtilsGeoJson.get_coordinates(permiso_menor.coordenada_x, permiso_menor.coordenada_y)

            GeoJson = {
                "type": "Feature",
                "id": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "OBJECTID": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                    "Usuario": permiso_menor.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Municipio": permiso_menor.cod_municipio.nombre,
                    "Latitud": lat,
                    "Longitud": lon,
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
            lat, lon = UtilsGeoJson.get_coordinates(permiso_menor.coordenada_x, permiso_menor.coordenada_y)

            GeoJson = {
                "type": "Feature",
                "id": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "OBJECTID": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                    "Nombre": "", # VALIDAR
                    "Numero_Matricula": "", # VALIDAR
                    "Numero_Codigo":"", # VALIDAR
                    "Latitud": lat,
                    "Longitud": lon, 
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
            lat, lon = UtilsGeoJson.get_coordinates(permiso_menor.coordenada_x, permiso_menor.coordenada_y)

            GeoJson = {
                "type": "Feature",
                "id": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
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
            lat, lon = UtilsGeoJson.get_coordinates(permiso_menor.coordenada_x, permiso_menor.coordenada_y)

            GeoJson = {
                "type": "Feature",
                "id": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "OBJECTID": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                    "Municipio" :permiso_menor.cod_municipio.nombre,
                    "Usuario": permiso_menor.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Latitud": lat,
                    "Longitud": lon,
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



class GeoJsonJardinesBotanicosView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        permisos_menores = PermisosAmbSolicitudesTramite.objects.filter(
            id_permiso_ambiental__cod_tipo_permiso_ambiental='PM',
            id_permiso_ambiental__nombre__icontains='Permiso ambiental de jardines botánicos'
        )

        GeoJson_list = []

        for permiso_menor in permisos_menores:
            # predios = Predios.objects.filter(id_solicitud_tramite=permiso_menor.id_solicitud_tramite)
            lat, lon = UtilsGeoJson.get_coordinates(permiso_menor.coordenada_x, permiso_menor.coordenada_y)

            # for predio in predios:
            GeoJson = {
                "type": "Feature",
                "id": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "OBJECTID": permiso_menor.id_solicitud_tramite.id_solicitud_tramite,
                    "Usuario": permiso_menor.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Matricula_Inmobiliaria": "", #predio.matricula_inmobiliaria, #VALIDAR
                    "Latitud": lat,
                    "Longitud": lon,
                    "Uso_Suelo_POT":"", # VALIDAR
                    "Area":"", # VALIDAR
                    "Nombre_Beneficiario":"", # VALIDAR
                    "Identificacion_Beneficiario":"", # VALIDAR
                    "Numero_Expediente": UtilsGeoJson.get_expediente(permiso_menor),
                    "Termino_Licencia": "", # VALIDAR
                    "Resolucion": "", # VALIDAR
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
