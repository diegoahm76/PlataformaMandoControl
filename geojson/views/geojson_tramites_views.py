import json
from rest_framework.exceptions import ValidationError,NotFound,PermissionDenied
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from geojson.utils import UtilsGeoJson
from geojson.models.tramites_models import PermisosAmbSolicitudesTramite

class GeoJsonDeterminantesAmbientalesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'DA')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [tramite_sasoftco['UbiEcosis'].split(',')[0], tramite_sasoftco['UbiEcosis'].split(',')[1]]
                    },
                    "properties": {
                        "municipio": tramite_sasoftco['MunPredio'],
                        "tipo_determinante": tramite_sasoftco['typeProcedure'],
                        "tipo_elementos_proteccion": tramite_sasoftco['Area'],
                        #"nombre_geografico": tramite.fecha_creacion, validar
                        #"area": tramite_sasoftco['ConceptP3'], Validar
                        "latitud": tramite_sasoftco['UbiEcosis'].split(',')[0],
                        "longitud": tramite_sasoftco['UbiEcosis'].split(',')[1],
                        "expediente": tramite_sasoftco['NumExp'],
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        #"resolucion": tramite_sasoftco['NumResol'], Validar
                        #"fecha_resolucion": tramite_sasoftco['Fecha_Resolu'], Validar
                        "estado": tramite.id_solicitud_tramite.id_estado_actual_solicitud.nombre,
                    }
                }

                hectareas = tramite_sasoftco['Levant_Catastral'] * 0.0001
                GeoJson['properties']['area'] = hectareas
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
    

class GeoJsonCertificacionAmbientalDesintegracionVehicularView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'CE', id_permiso_ambiental__nombre__icontains = 'Certificación ambiental para la desintegración vehicular')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [tramite_sasoftco['UbiEcosis'].split(',')[0], tramite_sasoftco['c'].split(',')[1]]
                    },
                    "properties": {
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        #"resolucion": tramite_sasoftco['NumResol'], Validar
                        "expediente": tramite_sasoftco['NumExp'],
                        #"vigencia": tramite_sasoftco['Vigencia'], #Validar
                        "fecha_expedicion_resolucion": tramite_sasoftco['Fecha_Resolu'], #Validar
                        "municipio": tramite_sasoftco['MunPredio'],
                        "fecha_inicio_vigencia": tramite_sasoftco['FechaIniVig'], #Validar
                        "latitud": tramite_sasoftco['UbiEcosis'].split(',')[0],
                        "longitud": tramite_sasoftco['UbiEcosis'].split(',')[1],
                        "nombre_proyecto": tramite_sasoftco['nameProject'],
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
    

class GeoJsonInscripcionGestorRCDView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'RE', id_permiso_ambiental__nombre__icontains = 'Registro de inscripción como gestor de residuos de construcción y demolición')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)

            if tramite_sasoftco:
                GeoJson = {
                    "Feature": tramite.id_permiso_ambiental.get_cod_tipo_permiso_ambiental_display(),
                    "geometry": {
                        "type": "Point",
                        "coordinates": [tramite.coordenada_x, tramite.coordenada_y]
                    },
                    "properties": {
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "municipio": tramite_sasoftco['Municipio'],
                        "nombre_proyecto": tramite_sasoftco['nameProject'],
                        "Latitud": tramite.coordenada_x,
                        "longitud": tramite.coordenada_y,
                        "fecha_incio_obra": tramite_sasoftco['FReserva_Inicial'],
                        "fecha_estimada_finalizacion": tramite_sasoftco['FReserva_Final'],
                        "rcd_susceptibles_aprovechamiento": tramite_sasoftco['procesoaprovechamiento'],#Validar
                        # "rcd_no_susceptibles_aprovechamiento": tramite_sasoftco['procesoaprovechamiento'],#Validar
                        "Fecha_Inscripcion": tramite.id_solicitud_tramite.fecha_registro.date(),

                        
                      
                    }
                }

                GeoJson_list.append(GeoJson)

        return Response(GeoJson_list)
    

class GeoJsonLicenciaAmbientalTransElectricaView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Licencias de líneas de transferencia eléctrica')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)

            if tramite_sasoftco:
                GeoJson = {
                    "Feature": tramite.id_permiso_ambiental.get_cod_tipo_permiso_ambiental_display(),
                    "geometry": {
                        "type": "Point",
                        "coordinates": [tramite.coordenada_x, tramite.coordenada_y]
                    },
                    "properties": {
                        # "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        # "municipio": tramite_sasoftco['Municipio'],
                        # "nombre_proyecto": tramite_sasoftco['nameProject'],
                        # "Latitud": tramite.coordenada_x,
                        # "longitud": tramite.coordenada_y,
                        # "fecha_incio_obra": tramite_sasoftco['FReserva_Inicial'],
                        # "fecha_estimada_finalizacion": tramite_sasoftco['FReserva_Final'],
                        # "rcd_susceptibles_aprovechamiento": tramite_sasoftco['procesoaprovechamiento'],#Validar
                        # # "rcd_no_susceptibles_aprovechamiento": tramite_sasoftco['procesoaprovechamiento'],#Validar
                        # "Fecha_Inscripcion": tramite.id_solicitud_tramite.fecha_registro.date(),

                        
                      
                    }
                }

                GeoJson_list.append(GeoJson)

        return Response(GeoJson_list)


class GeoJsonPermisoOcupacionCaucePlayaLechosView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', id_permiso_ambiental__nombre__icontains = 'Permiso de ocupación de cauce, playa y lechos')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)

            if tramite_sasoftco:
                GeoJson = {
                    "Feature": tramite.id_permiso_ambiental.get_cod_tipo_permiso_ambiental_display(),
                    "geometry": {
                        "type": "Point",
                        "coordinates": [tramite.coordenada_x, tramite.coordenada_y]
                    },
                    "properties": {
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "nro_matricula": tramite_sasoftco['MatriInmobi'],
                        "Latitud": tramite.coordenada_x,
                        "longitud": tramite.coordenada_y,
                        "municipio": tramite_sasoftco['Municipio'],
                        "nombre_proyecto": tramite_sasoftco['nameProject'],
                        "expediente": tramite_sasoftco['NumExp'],
                        "resolucion": tramite_sasoftco['resolucionFinal'],
                        "fecha_expedicion": tramite_sasoftco['Fecha_resolucion'],
                        "fecha_inicio_vigencia": tramite_sasoftco['FReserva_Inicial'],
                        "fecha_final_vigencia": tramite_sasoftco['FReserva_Final'],
                    }
                }

                GeoJson_list.append(GeoJson)

        return Response(GeoJson_list)



class GeoJsonPermisoVertimientosAguaView(generics.ListAPIView):

    def get(self, request):
        permisos_menores = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Permiso de vertimientos al agua')

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
                    "Nombre": permiso_menor.id_solicitud_tramite.nombre_proyecto,
                    "Matricula_Inmobiliaria": "", # VALIDAR
                    "Latitud": permiso_menor.coordenada_x,
                    "Longitud": permiso_menor.coordenada_y,
                    "Altura": "", # VALIDAR
                    "Municipio" :permiso_menor.cod_municipio.nombre,
                    "Usuario": permiso_menor.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Resolucion":"", # VALIDAR
                    "Fecha_Expedicion": "", # VALIDAR
                    "Numero_Expediente": UtilsGeoJson.get_expediente(permiso_menor),
                    "Termino_Permiso": "", # VALIDAR
                    "Fecha_Inicio": "", # VALIDAR
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


class GeoJsonPermisoVertimientosSueloView(generics.ListAPIView):

    def get(self, request):
        permisos_menores = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Permiso de vertimientos al suelo')

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
                    "Nombre": permiso_menor.id_solicitud_tramite.nombre_proyecto,
                    "Matricula_Inmobiliaria": "", # VALIDAR
                    "Cedula_Catastral": "", # VALIDAR
                    "Municipio" :permiso_menor.cod_municipio.nombre,
                    "Vereda": "", # VALIDAR
                    "Sector": "", # VALIDAR
                    "Usuario": permiso_menor.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Expediente": UtilsGeoJson.get_expediente(permiso_menor),
                    "Resolucion":"", # VALIDAR
                    "Fecha_Expedicion": "", # VALIDAR
                    "Termino_Permiso": "", # VALIDAR
                    "Fecha_Inicio": "", # VALIDAR
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


