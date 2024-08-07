import json
from rest_framework.exceptions import ValidationError,NotFound,PermissionDenied
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from geojson.models.radicados_models import PQRSDF
from geojson.utils import UtilsGeoJson
from geojson.models.tramites_models import PermisosAmbSolicitudesTramite
from geojson.models.viveros_models import Vivero
from django.db.models import Q

class GeoJsonDeterminantesAmbientalesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'DA')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite_sasoftco['UbiEcosis'].split(',')[0] if tramite_sasoftco.get('UbiEcosis') else "", tramite_sasoftco['UbiEcosis'].split(',')[1] if tramite_sasoftco.get('UbiEcosis') else "", True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "OBJECTID": tramite.id_solicitud_tramite.id_solicitud_tramite,
                        "municipio": tramite_sasoftco.get('MunPredio', ""),
                        "tipo_determinante": tramite_sasoftco.get('typeProcedure', ""),
                        "tipo_elementos_proteccion": tramite_sasoftco.get('Area', ""),
                        "nombre_geografico": "", # Validar
                        "area": "", # Validar
                        "latitud": lat,
                        "longitud": lon,
                        "expediente": tramite_sasoftco.get('NumExp', ""),
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "resolucion": "", # Validar
                        "fecha_resolucion": "", # Validar
                        "estado": tramite.id_solicitud_tramite.id_estado_actual_solicitud.nombre,
                    }
                }

                hectareas = tramite_sasoftco.get('Levant_Catastral') * 0.0001 if tramite_sasoftco.get('Levant_Catastral') else ""
                GeoJson['properties']['area'] = hectareas
                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
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
            lat, lon = UtilsGeoJson.get_coordinates(tramite_sasoftco['UbiEcosis'].split(',')[0] if tramite_sasoftco.get('UbiEcosis') else "", tramite_sasoftco['UbiEcosis'].split(',')[1] if tramite_sasoftco.get('UbiEcosis') else "", True)
 
            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "OBJECTID": tramite.id_solicitud_tramite.id_solicitud_tramite,
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "resolucion": "", # Validar
                        "expediente": tramite_sasoftco.get('NumExp', ""),
                        "vigencia": "", #Validar
                        "fecha_expedicion_resolucion": tramite_sasoftco.get('Fecha_Resolu', ""), #Validar
                        "municipio": tramite_sasoftco.get('MunPredio', ""),
                        "fecha_inicio_vigencia": tramite_sasoftco.get('FechaIniVig', ""), #Validar
                        "latitud": lat,
                        "longitud": lon,
                        "nombre_proyecto": tramite_sasoftco.get('nameProject', ""),
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
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
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "municipio": tramite_sasoftco.get('Municipio', ""),
                        "nombre_proyecto": tramite_sasoftco.get('nameProject', ""),
                        "Latitud": lat,
                        "longitud": lon,
                        "fecha_incio_obra": tramite_sasoftco.get('FReserva_Inicial', ""),
                        "fecha_estimada_finalizacion": tramite_sasoftco.get('FReserva_Final', ""),
                        "rcd_susceptibles_aprovechamiento": tramite_sasoftco.get('procesoaprovechamiento', ""), #Validar
                        "rcd_no_susceptibles_aprovechamiento": "", #Validar
                        "Fecha_Inscripcion": tramite.id_solicitud_tramite.fecha_registro.date(),

                        
                      
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    

class GeoJsonLicenciaAmbientalTransElectricaView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Licencias de hidrocarburos') # VALIDAR FILTRO

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Nombre": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "Nombre_Proyecto": tramite.id_solicitud_tramite.nombre_proyecto,
                        "Vigencia_Proyecto": "", # VALIDAR
                        "Resolucion": tramite_sasoftco.get('Resolucion_numero', ""),
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Vigencia": "", # VALIDAR
                        "Municipio": tramite.cod_municipio.nombre,
                        "Fecha_Expedicion_Resolucion": "", # VALIDAR
                        "Fecha_Exacta_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Finalizacion_Vigencia": tramite_sasoftco.get('FReserva_Final', "") # VALIDAR
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)


class GeoJsonPermisoOcupacionPlayaView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PA', id_permiso_ambiental__nombre__icontains = 'Permiso de ocupación de cauce, playa y lechos')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "nro_matricula": tramite_sasoftco.get('MatriInmobi', ""),
                        "Latitud": lat,
                        "longitud": lon,
                        "municipio": tramite_sasoftco.get('Municipio', ""),
                        "nombre_proyecto": tramite_sasoftco.get('nameProject', ""),
                        "expediente": tramite_sasoftco.get('NumExp', ""),
                        "resolucion": tramite_sasoftco.get('resolucionFinal', ""),
                        "fecha_expedicion": tramite_sasoftco.get('Fecha_resolucion', ""),
                        "fecha_inicio_vigencia": tramite_sasoftco.get('FReserva_Inicial', ""),
                        "fecha_final_vigencia": tramite_sasoftco.get('FReserva_Final', ""),
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)


class GeoJsonAprovechamientoCarbonVegetalMovilizacionView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', id_permiso_ambiental__nombre__icontains = 'Permiso para la producción y movilización de carbón vegetal con fines comerciales')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite_sasoftco['Mapa2'].split(',')[0] if tramite_sasoftco.get('Mapa2') else "", tramite_sasoftco['Mapa2'].split(',')[1] if tramite_sasoftco.get('Mapa2') else "")
 
            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "OBJECTID": tramite.id_solicitud_tramite.id_solicitud_tramite,
                        "codigo_catastral": tramite_sasoftco.get('CCatas', ""),
                        "numero_matricula": tramite_sasoftco.get('MatriInmobi', ""),
                        "municipio": tramite_sasoftco.get('MunPredio', ""),
                        "latitud": lat,
                        "longitud": lon,
                        "altura": tramite_sasoftco.get('Altura', ""), # Validar,
                        "Municipio": tramite_sasoftco.get('Municipio', ""),
                        "uso_suelo": "", # Validar,
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "expediente": tramite_sasoftco.get('NumExp', ""),
                        "resolucion": "", # Validar,
                        "expedicion": "", # validar,
                        "termino_permiso": "", #Validar
                        "fecha_fin_vigencia": "", #Validar
                        "fecha_inicio_vigencia": "", #Validar
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

class GeoJsonPermisoVertimientosAguaView(generics.ListAPIView):

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Permiso de vertimientos al agua')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            GeoJson = {
                "type": "Feature",
                "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "OBJECTID": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "Nombre": tramite.id_solicitud_tramite.nombre_proyecto,
                    "Matricula_Inmobiliaria": tramite_sasoftco.get('MatriInmobi', ""),
                    "Latitud": lat,
                    "Longitud": lon,
                    "Altura": "", # VALIDAR
                    "Municipio" :tramite.cod_municipio.nombre,
                    "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Resolucion":"", # VALIDAR
                    "Fecha_Expedicion": "", # VALIDAR
                    "Expediente": UtilsGeoJson.get_expediente(tramite),
                    "Termino_Permiso": "", # VALIDAR
                    "Fecha_Inicio": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                    "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', ""), # VALIDAR
                }
            }
            GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        print("geojson_final: ", GeoJson_list)

        return Response(geojson_final)


class GeoJsonAprovechamientoProductosForestalesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', id_permiso_ambiental__nombre__icontains = 'Permiso de aprovechamiento de productos forestales no maderables (PFNM)')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite_sasoftco['LatitudF'].split(',')[0] if tramite_sasoftco.get('LatitudF') else "", tramite_sasoftco['LatitudF'].split(',')[1] if tramite_sasoftco.get('LatitudF') else "", True)
 
            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "OBJECTID": tramite.id_solicitud_tramite.id_solicitud_tramite,
                        "numero_matricula": tramite_sasoftco.get('MatriInmobi', ""),
                        "municipio": tramite_sasoftco.get('MunPredio', ""),
                        "latitud": lat,
                        "longitud": lon,
                        "altura": "", # Validar
                        "Municipio": tramite_sasoftco.get('MunPredio', ""),
                        "uso_suelo": "", # Validar
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "expediente": tramite_sasoftco.get('NumExp', ""),
                        "resolucion": "", # Validar
                        "fecha_expedicion": "", # validar
                        "termino_permiso": "", #Validar
                        "vigencia": "", #Validars
                        "fecha_fin_vigencia": "", #Validar
                        "fecha_inicio_vigencia": "", #Validar
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    
class GeoJsonPermisoVertimientosSueloView(generics.ListAPIView):

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Permiso de vertimientos al suelo')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            GeoJson = {
                "type": "Feature",
                "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "OBJECTID": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "Nombre": tramite.id_solicitud_tramite.nombre_proyecto,
                    "Matricula_Inmobiliaria": tramite_sasoftco.get('MatriInmobi', ""),
                    "Cedula_Catastral": tramite_sasoftco.get('CCatas', ""),
                    "Municipio" :tramite.cod_municipio.nombre,
                    "Vereda": tramite_sasoftco.get('Ndivision', ""),
                    "Sector": "", # VALIDAR
                    "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Expediente": UtilsGeoJson.get_expediente(tramite),
                    "Resolucion":"", # VALIDAR
                    "Fecha_Expedicion": "", # VALIDAR
                    "Termino_Permiso": "", # VALIDAR
                    "Fecha_Inicio": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                    "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', ""), # VALIDAR
                }
            }
            GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    
class GeoJsonPermisosProspeccionAguasSubterraneasView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', id_permiso_ambiental__nombre__icontains = 'Permiso de Prospección y exploración de aguas subterráneas')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Numero_Matricula_Inmobiliaria": tramite_sasoftco.get('MatriInmobi', ""),
                        "Cedula_Catastral": tramite_sasoftco.get('CCatas', ""),
                        "Vereda": tramite_sasoftco.get('Ndivision', ""),
                        "Sector": tramite_sasoftco.get('Zon_value', ""),
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Resolucion": "", # VALIDAR
                        "Fecha_Expedicion": "", # VALIDAR
                        "Termino_Permiso": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', ""), # VALIDAR
                        "Latitud": lat,
                        "Longitud": lon,
                        "Altura": "", # VALIDAR
                        "Pozo_Profundo_Construido": "", # VALIDAR
                        "Proyeccion_Uso": "", # VALIDAR
                    }
                }
                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    
class GeoJsonPlanesContingenciaEstacionesServicioView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PR', id_permiso_ambiental__nombre__icontains = 'Proceso de Revisión y Seguimiento para elaboración de planes de Contingencia para el manejo de derrames de hidrocarburos o sustancias nocivas (transporte)')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Nombre_Estacion_Servicio": tramite_sasoftco.get("Npredio1", ""), # VALIDAR
                        "Numero_Matricula_Inmobiliaria": tramite_sasoftco.get('MatriInmobi', ""),
                        "Latitud": lat,
                        "Longitud": lon,
                        "Altura": "", # VALIDAR
                        "Municipio" :tramite.cod_municipio.nombre,
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Resolucion": "", # VALIDAR
                        "Fecha_Expedicion": "", # VALIDAR
                        "Termino_Permiso": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', ""), # VALIDAR
                    }
                }
                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    
class GeoJsonProyectosIndustrialesMineriasView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', id_permiso_ambiental__nombre__icontains = 'Permiso para proyectos industriales asociados a minería')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Nombre": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "Numero_Identificacion": tramite.id_solicitud_tramite.id_persona_titular.numero_documento,
                        "Actividad_Industrial": tramite.id_solicitud_tramite.nombre_proyecto,
                        "Vigencia_Permiso": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', ""), # VALIDAR
                        "Municipio" :tramite.cod_municipio.nombre
                    }
                }
                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)

class GeoJsonPermisoOcupacionCaucesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PA', id_permiso_ambiental__nombre__icontains = 'Permiso de ocupación de cauce, playa y lechos') # VALIDAR SI TOCA HACER OTRO FILTRO PARA SOLO CAUCES

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Nombre": tramite.id_solicitud_tramite.nombre_proyecto,
                        "Numero_Matricula": tramite_sasoftco.get('MatriInmobi', ""),
                        "Latitud": lat,
                        "Longitud": lon,
                        "Altura": tramite_sasoftco.get('Altura_m', ""),
                        "Municipio" :tramite.cod_municipio.nombre,
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Resolucion": tramite_sasoftco.get('Resolucion_numero', ""),
                        "Expedicion": "", # VALIDAR
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Termino_Permiso": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', ""), # VALIDAR
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    
class GeoJsonRecoleccionEspecimenesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', id_permiso_ambiental__nombre__icontains = 'Permiso de recolección de especímenes de especies silvestres de la diversidad biológica con fines de investigación científica no comercial')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Municipio" :tramite.cod_municipio.nombre,
                        "Latitud": lat,
                        "Longitud": lon,
                        "Resolucion": tramite_sasoftco.get('resolucion', ""), # VALIDAR
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Vigencia": "", # VALIDAR
                        "Fecha_Expedicion_Resolucion": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Especimen": "", # VALIDAR
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    
class GeoJsonCertificacionAmbientalAutomotoresView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'CE', id_permiso_ambiental__nombre__icontains = 'Certificación ambiental para la habilitación de los centros de diagnóstico automotor')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Latitud": lat,
                        "Longitud": lon,
                        "Resolucion": "", # VALIDAR
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Descripcion_Vigencia": "", # VALIDAR
                        "Fecha_Expedicion_Resolucion": "", # VALIDAR
                        "Fecha_Exacta_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Nombre_CDA": tramite.id_solicitud_tramite.nombre_proyecto, # tramite_sasoftco.get('Npredio'] # VALIDAR
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    
class GeoJsonPermisoEmisionesAtmosfericasView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Permiso de emisiones atmosféricas')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Nombre_Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Numero_Resolucion": tramite_sasoftco.get('Num_resolucion', ""), # VALIDAR
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Vigencia": "", # VALIDAR
                        "Tipo_Combustible": tramite_sasoftco.get('Combustible', "") if tramite_sasoftco.get('Combustible') and tramite_sasoftco.get('Combustible') != 'Otro' else tramite_sasoftco.get('Cual3', ""),
                        "Expedicion": "", # VALIDAR
                        "Latitud": lat,
                        "Longitud": lon,
                        "Nombre_Fuente": tramite.id_solicitud_tramite.nombre_proyecto, # tramite_sasoftco.get('Npredio'] # VALIDAR
                        "Fuente_Emision": tramite_sasoftco.get('Emission_source_type', "") if tramite_sasoftco.get('Emission_source_type') and tramite_sasoftco.get('Emission_source_type') != 'Otro' else tramite_sasoftco.get('Cual1', ""),
                        "Linea_Produccion": "", # VALIDAR
                        "Produccion_Anual": "", # VALIDAR
                        "Capacidad_Instalada": "", # VALIDAR
                        "Equipo_Control": tramite_sasoftco.get('Equipo_Control', "") if tramite_sasoftco.get('Equipo_Control') and tramite_sasoftco.get('Equipo_Control') != 'Otro' else tramite_sasoftco.get('Cual2', "")
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    
class GeoJsonInscripcionAcopiadorAceitesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'RE', id_permiso_ambiental__nombre__icontains = 'Registro de Inscripción de acopiadores primarios de aceites lubricantes usados')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Numero_Resolucion": "", # VALIDAR
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Vigencia": "", # VALIDAR
                        "Fecha_Exacta_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Expedicion_Resolucion": "", # VALIDAR
                        "Latitud": lat,
                        "Longitud": lon,
                        "Volumen_Aceite_Almacenado": tramite_sasoftco.get('Volac', ""),
                        "Tipo_Acopiador": tramite_sasoftco.get('Tacop_value') if tramite_sasoftco.get('Tacop_value') and tramite_sasoftco.get('Tacop_value') != 'Otro' else tramite_sasoftco.get('Tacop2', ""),
                        "Tipo_Aceite_Usado": tramite_sasoftco.get('Toil_value') if tramite_sasoftco.get('Toil_value') and tramite_sasoftco.get('Toil_value') != 'Otro' else tramite_sasoftco.get('Toil2', ""),
                        "Sistema_Almacenamiento_Residuos": tramite_sasoftco.get('Sisalm_value') if tramite_sasoftco.get('Sisalm_value') and tramite_sasoftco.get('Sisalm_value') != 'Otro' else tramite_sasoftco.get('Sisalm2', "")
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    
class GeoJsonPQRSDFView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        pqrsdfs = PQRSDF.objects.all()

        GeoJson_list = []

        for pqrsdf in pqrsdfs:
            lat, lon = UtilsGeoJson.get_coordinates(pqrsdf.id_sucursal_especifica_implicada.direccion_sucursal_georeferenciada_lat, pqrsdf.id_sucursal_especifica_implicada.direccion_sucursal_georeferenciada_lon)

            GeoJson = {
                "type": "Feature",
                "id": pqrsdf.id_PQRSDF,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "Municipio" : pqrsdf.id_sucursal_especifica_implicada.municipio.nombre, # VALIDAR
                    "Tipo_Solicitud": pqrsdf.get_cod_tipo_PQRSDF_display(),
                    "Recurso_Afectado": "", # VALIDAR
                    "Zona": "", # VALIDAR
                    "Departamento": pqrsdf.id_sucursal_especifica_implicada.municipio.cod_departamento.nombre, # VALIDAR
                    "Fecha_Registro": pqrsdf.fecha_registro,
                    "Solicitud": pqrsdf.descripcion,
                    "Estado": pqrsdf.id_estado_actual_solicitud.nombre,
                    "Grupo": pqrsdf.id_persona_titular.id_unidad_organizacional_actual.nombre if pqrsdf.id_persona_titular and pqrsdf.id_persona_titular.id_unidad_organizacional_actual else "", # VALIDAR
                    "Fecha_Inicio_Vigencia": "", # VALIDAR
                    "Fecha_Fin_Vigencia": "", # VALIDAR
                    "Tema": pqrsdf.asunto,
                    "Medio_Interposicion": pqrsdf.id_medio_solicitud.nombre,
                    "Tipo_Persona": pqrsdf.id_persona_titular.get_tipo_persona_display() if pqrsdf.id_persona_titular else "", # VALIDAR
                    "Medio_Respuesta": "", # VALIDAR
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

class GeoJsonReporteViveroView(generics.ListAPIView):

    def get(self, request):
        viveros = Vivero.objects.all()

        GeoJson_list = []

        for vivero in viveros:
            lat, lon = UtilsGeoJson.get_coordinates(vivero.coordenadas_lat, vivero.coordenadas_lon)

            GeoJson = {
                "type": "Feature",
                "id": vivero.id_vivero,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "OBJECTID": vivero.id_vivero,
                    "nombre":vivero.nombre,
                    "cod_municipio":vivero.cod_municipio.nombre,
                    "direccion":vivero.direccion,
                    "coordenadas_lat":vivero.coordenadas_lat,
                    "coordenadas_lon":vivero.coordenadas_lon,
                    "area_mt2":vivero.area_mt2,
                    "area_propagacion_mt2":vivero.area_propagacion_mt2,
                    "tiene_area_produccion":vivero.tiene_area_produccion,
                    "tiene_areas_pep_sustrato":vivero.tiene_areas_pep_sustrato,
                    "tiene_area_embolsado":vivero.tiene_area_embolsado,
                    "cod_tipo_vivero":vivero.cod_tipo_vivero,
                    "id_viverista_actual":vivero.id_viverista_actual.id_persona if vivero.id_viverista_actual else "",
                    "fecha_inicio_viverista_actual":vivero.fecha_inicio_viverista_actual if vivero.fecha_inicio_viverista_actual else "",
                    "cod_origen_recursos_vivero":vivero.cod_origen_recursos_vivero if vivero.cod_origen_recursos_vivero else "",
                    "fecha_creacion":vivero.fecha_creacion if vivero.fecha_creacion else "",
                    "id_persona_crea":vivero.id_persona_crea.id_persona if vivero.id_persona_crea else "",
                    "en_funcionamiento":vivero.en_funcionamiento if vivero.en_funcionamiento else "",
                    "fecha_ultima_apertura":vivero.fecha_ultima_apertura if vivero.fecha_ultima_apertura else "",
                    "id_persona_abre":vivero.id_persona_abre.id_persona if vivero.id_persona_abre else "",
                    "justificacion_apertura":vivero.justificacion_apertura if vivero.justificacion_apertura else "",
                    "fecha_cierre_actual":vivero.fecha_cierre_actual if vivero.fecha_cierre_actual else "",
                    "id_persona_cierra":vivero.id_persona_cierra.id_persona if vivero.id_persona_cierra else "",
                    "justificacion_cierre":vivero.justificacion_cierre if vivero.justificacion_cierre else "",
                    "vivero_en_cuarentena":vivero.vivero_en_cuarentena if vivero.vivero_en_cuarentena else "",
                    "fecha_inicio_cuarentena":vivero.fecha_inicio_cuarentena if vivero.fecha_inicio_cuarentena else "",
                    "id_persona_cuarentena":vivero.id_persona_cuarentena.id_persona if vivero.id_persona_cuarentena else "",
                    "justificacion_cuarentena":vivero.justificacion_cuarentena if vivero.justificacion_cuarentena else "",
                    "ruta_archivo_creacion":vivero.ruta_archivo_creacion.ruta_archivo.url if vivero.ruta_archivo_creacion else "",
                    "activo":vivero.activo,
                    "item_ya_usado":vivero.item_ya_usado,
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
    

class GeoJsonAlmacenamientoSustanciasNocivasView(generics.ListAPIView):

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Licencias de hidrocarburos') # VALIDAR FILTRO

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            GeoJson = {
                "type": "Feature",
                "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "OBJECTID": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Resolucion": tramite_sasoftco.get('Resolucion_numero', ""),
                    "Expediente": UtilsGeoJson.get_expediente(tramite),
                    "Fecha_Expedicion": "", # VALIDAR
                    "Termino_Otorga_Permiso": "", # VALIDAR
                    "Fecha_Exacta_Inicio_Vigencia": "", # VALIDAR
                    "Fecha_Exacta_Finalizacion_Vigencia": "", # VALIDAR
                    "Municipio" :tramite.cod_municipio.nombre
                }
            }
            GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    

class GeoJsonRegistroLibroOperacionesView(generics.ListAPIView):

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'RE', id_permiso_ambiental__nombre__icontains = 'Registro de libro de operaciones de industrias forestales')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            GeoJson = {
                "type": "Feature",
                "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "OBJECTID": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "Nombre_Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                    "Municipio" :tramite.cod_municipio.nombre,
                    "Latitud": lat,
                    "Longitud": lon,
                    "Esquema_Reconocimiento": "", # VALIDAR
                    "Resolucion":"", # VALIDAR
                    "Expedicion": "", # VALIDAR
                    "Vigencia": "", # VALIDAR
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
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)


class GeoJsonAprovechamientoForestalView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):

        tramites = PermisosAmbSolicitudesTramite.objects.filter(
            Q(id_permiso_ambiental__cod_tipo_permiso_ambiental='PE') & (
                Q(id_permiso_ambiental__nombre__icontains='Permiso aprovechamiento forestal aislado') &
                Q(id_permiso_ambiental__nombre__icontains='Permiso aprovechamiento forestal persistente') &
                Q(id_permiso_ambiental__nombre__icontains='Permiso de aprovechamiento forestal')
            )
        )

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Nombre": tramite_sasoftco.get('nameProject', ""),
                        "Numero_Matricula": tramite_sasoftco.get('MatriInmobi', ""),
                        'Nro_Codigo':"",
                        "Altura": "", # VALIDAR
                        "Latitud": lat,
                        "Longitud": lon,   
                        "Municipio": tramite_sasoftco.get('MunPredio', ""),
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Resolucion": "", # VALIDAR
                        "Uso_Suelo_POT": tramite_sasoftco.get('Uso_suelo', ""), # VALIDAR 
                        "Fecha_Expedicion_Resolucion": "", # VALIDAR
                        "Fecha_Expedicion": "", # VALIDAR
                        "Expedicion": "", # VALIDAR
                        "Vigencia": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', ""), # VALIDAR

                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    



class GeoJsonAprovechamientoForestalDomesticoView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', 
                                                                id_permiso_ambiental__nombre__icontains = 'Permiso de aprovechamiento forestal doméstico')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Nombre": tramite_sasoftco.get('nameProject', ""),
                        "Numero_Matricula": tramite_sasoftco.get('MatriInmobi', ""),
                        'Nro_Codigo':"",
                        "Latitud": lat,
                        "Longitud": lon,  
                        "Altura": "", # VALIDAR 
                        "Municipio": tramite_sasoftco.get('MunPredio', ""),
                        "Uso_Suelo_POT": "", # VALIDAR 
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Resolucion": "", # VALIDAR
                        "Fecha_Expedicion": "", # VALIDAR
                        "Expedicion": "", # VALIDAR
                        "Vigencia": "", # VALIDAR
                        "Fecha_Expedicion_Resolucion": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', ""), # VALIDAR
                                             
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    
    

class GeoJsonSolicitudDeterminantesAmbientalesPlanesParcialesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PR', 
                                                                id_permiso_ambiental__nombre__icontains = 'Solicitud de determinantes ambientales planes parciales')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Nombre_geo": tramite_sasoftco.get('nameProject', ""),#Validar
                        "Tipo_determinante": tramite_sasoftco.get('typeProcedure', ""),
                        'Nro_Codigo':"",
                        "Area": "", # VALIDAR   
                        "Latitud": lat,
                        "Longitud": lon,  
                        "Altura": "", # VALIDAR   
                        "Municipio": tramite_sasoftco.get('MunPredio', ""),  
                        "Expediente":tramite_sasoftco.get('NumExp', ""), 
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Resolucion": "", # VALIDAR
                        "Fecha_Resolucion": "", # VALIDAR
                        "Estado": tramite_sasoftco.get('Estado', ""),
                        "Tipo": tramite_sasoftco.get('TypePermiso', "")# VALIDAR
                                             
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)

class GeoJsonConcesionAguasSuperficialesView(generics.ListAPIView):

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Concesión para el uso de aguas superficiales')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite_sasoftco['Mapa2'].split(',')[0] if tramite_sasoftco.get('Mapa2') else "", tramite_sasoftco['Mapa2'].split(',')[1] if tramite_sasoftco.get('Mapa2') else "", True)
 
            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "OBJECTID": tramite.id_solicitud_tramite.id_solicitud_tramite,
                        "matricula_inmobiliaria": tramite_sasoftco.get('MatriInmobi', ""),
                        "latitud": lat,
                        "altura": tramite_sasoftco.get('Altura_mnsnm', ""),
                        "municipio": tramite_sasoftco.get('Mun_fuente', ""),
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "resolucion": tramite_sasoftco.get('NumResol', ""),
                        "fecha_expedicion": tramite_sasoftco.get('Fecha_Resolu', ""),
                        "expediente": tramite_sasoftco.get('NumExp', ""),
                        "termino_permiso": tramite_sasoftco.get('FechaIniVig', ""), # validar
                        "fecha_inicio_vigencia": tramite_sasoftco.get('FechaIniVig', ""), # validar
                        "fecha_fin_vigencia": tramite_sasoftco.get('FechaFinVig', ""), # validar
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    

class GeoJsonConcesionAguasSubterraneasView(generics.ListAPIView):

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Concesión de aguas subterráneas')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite_sasoftco['Mapa2'].split(',')[0] if tramite_sasoftco.get('Mapa2') else "", tramite_sasoftco['Mapa2'].split(',')[1] if tramite_sasoftco.get('Mapa2') else "", True)
 
            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "OBJECTID": tramite.id_solicitud_tramite.id_solicitud_tramite,
                        "matricula_inmobiliaria": tramite_sasoftco.get('MatriInmobi', ""),
                        "cedula_catastral": tramite_sasoftco.get('CCatas', ""),
                        "municipio": tramite_sasoftco.get('Mun_fuente', ""),
                        "vereda": tramite_sasoftco.get('Ndivision', ""),
                        "sector": "", # Validar
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "resolucion": tramite_sasoftco.get('Resolu_Text', ""),
                        "expediente": tramite_sasoftco.get('NumExp', ""),
                        "fecha_expedicion": "", # Validar
                        "termino_permiso": "", # validar
                        "fecha_inicio_vigencia": tramite_sasoftco.get('Fech_Exp_Legal_Point', ""),
                        "fecha_fin_vigencia": tramite_sasoftco.get('Fech_Venci_Legal_Pont', ""),
                        "fuente_captacion": tramite_sasoftco.get('Name_fuente_hidrica1', ""),
                        "uso_recurso": tramite_sasoftco.get('Usos_Water_Table1', ""),
                        "profundidad": tramite_sasoftco.get('Profun_Point_Succ', ""),
                        "latitud": lat,
                        "longitud": lon,
                        "altura": "", # Validar
                        "numero_identificador_pozo": "", # validar
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }

        return Response(geojson_final)
    
class GeoJsonExpedientesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites_expedientes = PermisosAmbSolicitudesTramite.objects.exclude(id_solicitud_tramite__id_expediente = None)

        GeoJson_list = []

        for tramite_expediente in tramites_expedientes:
            expediente = tramite_expediente.id_solicitud_tramite.id_expediente
            lat, lon = UtilsGeoJson.get_coordinates(tramite_expediente.coordenada_x, tramite_expediente.coordenada_y)

            GeoJson = {
                "type": "Feature",
                "id": expediente.id_expediente_documental,
                "geometry": {
                    "type": "Point",
                    "coordinates": [lat, lon]
                },
                "properties": {
                    "Municipio" : tramite_expediente.cod_municipio.nombre,
                    "Departamento": tramite_expediente.cod_municipio.cod_departamento.nombre,
                    "Estado": tramite_expediente.id_solicitud_tramite.id_estado_actual_solicitud.nombre,
                    "Tipo_Tramite": tramite_expediente.id_permiso_ambiental.get_cod_tipo_permiso_ambiental_display(),
                    "Fecha": tramite_expediente.id_solicitud_tramite.fecha_expediente
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

class GeoJsonLicenciaAmbientalNoConvencionalView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Licencias de hidrocarburos') # VALIDAR FILTRO

    def get(self, request):
        tramites = self.queryset.all()

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "nombre_proyecto": tramite_sasoftco.get('nameProject', ""),
                        "municipio": tramite_sasoftco.get('Municipio', ""),
                        "vigencia_proyecto": "", # Validar
                        "resolucion": tramite_sasoftco.get('Resolucion_numero', ""),
                        "expediente": tramite_sasoftco.get('NumExp', ""),
                        "vigencia": "", # Validar
                        "fecha_expedicion_resolucion": tramite_sasoftco.get('Fecha_resolucion', ""),
                        "fecha_inicio_vigencia": tramite_sasoftco.get('FReserva_Inicial', ""),#Validar
                        "fecha_final_vigencia": tramite_sasoftco.get('FReserva_Final', ""),#Validar 
                        "Latitud": lat,
                        "Longitud": lon                            
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }
    
        return Response(geojson_final)

class GeoJsonLicenciaAmbientalTransferenciaFotovoltaicaView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Licencias de hidrocarburos') # VALIDAR FILTRO

    def get(self, request):
        tramites = self.queryset.all()

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Nombre": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "Nombre_Proyecto": tramite.id_solicitud_tramite.nombre_proyecto,
                        "Vigencia_Proyecto": "", # VALIDAR
                        "Resolucion": tramite_sasoftco.get('Resolucion_numero', ""),
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Vigencia": "", # VALIDAR
                        "Fecha_Expedicion": "", # VALIDAR
                        "Fecha_Inicio": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', ""), # VALIDAR 
                        "Municipio": tramite.cod_municipio.nombre,                 
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }
    
        return Response(geojson_final)

class GeoJsonLicenciaAmbientalRellenosSanitariosView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Licencia ambiental aire y urbano')

    def get(self, request):
        tramites = self.queryset.all()

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco and 'rellenos' in tramite_sasoftco.get('TipPermi', ""):
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Numero_Matricula": tramite_sasoftco.get('MatriInmobi', ""),
                        "Nombre_Proyecto": tramite.id_solicitud_tramite.nombre_proyecto,
                        "Latitud": lat,
                        "Longitud": lon,
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Vigencia": "", # VALIDAR
                        "Fecha_Expedicion": "", # VALIDAR
                        "Fecha_Inicio": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', ""), # VALIDAR 
                        "Municipio": tramite.cod_municipio.nombre
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }
    
        return Response(geojson_final)

class GeoJsonLicenciaAmbientalAprovechamientoResiduosOrganicosView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Licencia ambiental aire y urbano')

    def get(self, request):
        tramites = self.queryset.all()

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco and 'residuos' in tramite_sasoftco.get('TipPermi', ""):
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Nombre_Proyecto": tramite.id_solicitud_tramite.nombre_proyecto,
                        "Numero_Matricula": tramite_sasoftco.get('MatriInmobi', ""),
                        "Latitud": lat,
                        "Longitud": lon,
                        "Altura": tramite_sasoftco.get('Altura_m', ""),
                        "Municipio": tramite.cod_municipio.nombre,
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Resolucion": tramite_sasoftco.get('Resolucion_numero', ""),
                        "Fecha_Expedicion": "", # VALIDAR
                        "Termino_Permiso": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', ""), # VALIDAR 
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }
    
        return Response(geojson_final)

class GeoJsonMedidasManejoAmbientalView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'EM', id_permiso_ambiental__nombre__icontains = 'Evaluación de medidas de manejo ambiental para proyectos sísmicos')

    def get(self, request):
        tramites = self.queryset.all()

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
            lat, lon = UtilsGeoJson.get_coordinates(tramite.coordenada_x, tramite.coordenada_y, True)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lat, lon]
                    },
                    "properties": {
                        "Nombre": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "Nombre_Proyecto": tramite.id_solicitud_tramite.nombre_proyecto,
                        "Vigencia_Proyecto": "", # VALIDAR
                        "Resolucion": tramite_sasoftco.get('Resolucion_numero', ""),
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Fecha_Expedicion_Resolucion": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco.get('FReserva_Inicial', ""), # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco.get('FReserva_Final', "") # VALIDAR
                    }
                }

                GeoJson_list.append(GeoJson)

        geojson_final = {
            "type": "FeatureCollection",
            "crs": { 
                "type": "name", 
                "properties": { 
                    "name": "EPSG:9377" 
                } 
            },
            "features": GeoJson_list
        }
    
        return Response(geojson_final)

