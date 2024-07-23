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


class GeoJsonPermisoOcupacionPlayaView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PA', id_permiso_ambiental__nombre__icontains = 'Permiso de ocupación de cauce, playa y lechos')

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


class GeoJsonAprovechamientoCarbonVegetalMovilizacionView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', id_permiso_ambiental__nombre__icontains = 'Permiso para la producción y movilización de carbón vegetal con fines comerciales')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
 
            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [tramite_sasoftco['Mapa2'].split(',')[0], tramite_sasoftco['Mapa2'].split(',')[1]]
                    },
                    "properties": {
                        "codigo_catastral": tramite_sasoftco['CCatas'],
                        "numero_matricula": tramite_sasoftco['MatriInmobi1'],
                        "municipio": tramite_sasoftco['MunPredio'],
                        "latitud": tramite_sasoftco['Mapa2'].split(',')[0],
                        "longitud": tramite_sasoftco['Mapa2'].split(',')[1],
                        #"altura": tramite_sasoftco['Altura'] Validar,
                        "Municipio": tramite_sasoftco['Municipio'],
                        #"uso_suelo": tramite_sasoftco['UsoSuelo'] Validar,
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "expediente": tramite_sasoftco['NumExp'],
                        #"resolucion": tramite_sasoftco['NumResol'] Validar,
                        #"expedicion": tramite_sasoftco['Fecha_Resolu'] validar,
                        #"termino_permiso": tramite_sasoftco['FechaIniVig'], #Validar
                        #"fecha_fin_vigencia": tramite_sasoftco['FechaFinVig'], #Validar
                        #"fecha_inicio_vigencia": tramite_sasoftco['FechaIniVig'], #Validar
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


class GeoJsonAprovechamientoProductosForestalesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', id_permiso_ambiental__nombre__icontains = 'Permiso de aprovechamiento de productos forestales no maderables (PFNM)')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)
 
            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [tramite_sasoftco['LatitudF'].split(',')[0], tramite_sasoftco['LatitudF'].split(',')[1]]
                    },
                    "properties": {
                        "numero_matricula": tramite_sasoftco['MatriInmobi'],
                        "municipio": tramite_sasoftco['MunPredio'],
                        "latitud": tramite_sasoftco['LatitudF'].split(',')[0],
                        "longitud": tramite_sasoftco['LatitudF'].split(',')[1],
                        #"altura": tramite_sasoftco['Altura'] Validar,
                        "Municipio": tramite_sasoftco['MunPredio'],
                        #"uso_suelo": tramite_sasoftco['UsoSuelo'] Validar,
                        "usuario": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "expediente": tramite_sasoftco['NumExp'],
                        #"resolucion": tramite_sasoftco['NumResol'] Validar,
                        #"fecha_expedicion": tramite_sasoftco['Fecha_Resolu'] validar,
                        #"termino_permiso": tramite_sasoftco['FechaIniVig'], #Validar
                        #"vigencia": tramite_sasoftco['FechaFinVig'], #Validars
                        #"fecha_fin_vigencia": tramite_sasoftco['FechaFinVig'], #Validar
                        #"fecha_inicio_vigencia": tramite_sasoftco['FechaIniVig'], #Validar
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
    
class GeoJsonPermisosProspeccionAguasSubterraneasView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', id_permiso_ambiental__nombre__icontains = 'Permiso de Prospección y exploración de aguas subterráneas')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [tramite.coordenada_x, tramite.coordenada_y]
                    },
                    "properties": {
                        "Numero_Matricula_Inmobiliaria": tramite_sasoftco['MatriInmobi'],
                        "Cedula_Catastral": tramite_sasoftco['CCatas'],
                        "Vereda": tramite_sasoftco['Ndivision'],
                        "Sector": tramite_sasoftco['Zon_value'],
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Resolucion": "", # VALIDAR
                        "Fecha_Expedicion": "", # VALIDAR
                        "Termino_Permiso": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco['FReserva_Inicial'], # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco['FReserva_Final'], # VALIDAR
                        "Latitud": tramite.coordenada_x,
                        "Longitud": tramite.coordenada_y,
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
                    "name": "EPSG:4326" 
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

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [tramite.coordenada_x, tramite.coordenada_y]
                    },
                    "properties": {
                        "Nombre_Estacion_Servicio": tramite_sasoftco["Npredio1"], # VALIDAR
                        "Numero_Matricula_Inmobiliaria": tramite_sasoftco['MatriInmobi'],
                        "Latitud": tramite.coordenada_x,
                        "Longitud": tramite.coordenada_y,
                        "Altura": "", # VALIDAR
                        "Municipio" :tramite.cod_municipio.nombre,
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Resolucion": "", # VALIDAR
                        "Fecha_Expedicion": "", # VALIDAR
                        "Termino_Permiso": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco['FReserva_Inicial'], # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco['FReserva_Final'], # VALIDAR
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
    
class GeoJsonProyectosIndustrialesMineriasView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', id_permiso_ambiental__nombre__icontains = 'Permiso para proyectos industriales asociados a minería')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)

            if tramite_sasoftco:
                GeoJson = {
                    "type": "Feature",
                    "id": tramite.id_solicitud_tramite.id_solicitud_tramite,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [tramite.coordenada_x, tramite.coordenada_y]
                    },
                    "properties": {
                        "Nombre": UtilsGeoJson.get_nombre_persona(tramite.id_solicitud_tramite.id_persona_titular),
                        "Numero_Identificacion": tramite.id_solicitud_tramite.id_persona_titular.numero_documento,
                        "Actividad_Industrial": tramite.id_solicitud_tramite.nombre_proyecto,
                        "Vigencia_Permiso": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco['FReserva_Inicial'], # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco['FReserva_Final'], # VALIDAR
                        "Municipio" :tramite.cod_municipio.nombre
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

class GeoJsonPermisoOcupacionCaucesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PA', id_permiso_ambiental__nombre__icontains = 'Permiso de ocupación de cauce, playa y lechos') # VALIDAR SI TOCA HACER OTRO FILTRO PARA SOLO CAUCES

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
                        "Nombre": tramite.id_solicitud_tramite.nombre_proyecto,
                        "Numero_Matricula": tramite_sasoftco['MatriInmobi'],
                        "Latitud": tramite.coordenada_x,
                        "Longitud": tramite.coordenada_y,
                        "Altura": tramite_sasoftco['Altura_m'],
                        "Municipio" :tramite.cod_municipio.nombre,
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Resolucion": tramite_sasoftco['Resolucion_numero'],
                        "Expedicion": "", # VALIDAR
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Termino_Permiso": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco['FReserva_Inicial'], # VALIDAR
                        "Fecha_Fin_Vigencia": tramite_sasoftco['FReserva_Final'], # VALIDAR
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
    
class GeoJsonRecoleccionEspecimenesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'PE', id_permiso_ambiental__nombre__icontains = 'Permiso de recolección de especímenes de especies silvestres de la diversidad biológica con fines de investigación científica no comercial')

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
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Municipio" :tramite.cod_municipio.nombre,
                        "Latitud": tramite.coordenada_x,
                        "Longitud": tramite.coordenada_y,
                        "Resolucion": tramite_sasoftco['resolucion'], # VALIDAR
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Vigencia": "", # VALIDAR
                        "Fecha_Expedicion_Resolucion": "", # VALIDAR
                        "Fecha_Inicio_Vigencia": tramite_sasoftco['FReserva_Inicial'], # VALIDAR
                        "Especimen": "", # VALIDAR
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
    
class GeoJsonCertificacionAmbientalAutomotoresView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'CE', id_permiso_ambiental__nombre__icontains = 'Certificación ambiental para la habilitación de los centros de diagnóstico automotor')

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
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Latitud": tramite.coordenada_x,
                        "Longitud": tramite.coordenada_y,
                        "Resolucion": "", # VALIDAR
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Descripcion_Vigencia": "", # VALIDAR
                        "Fecha_Expedicion_Resolucion": "", # VALIDAR
                        "Fecha_Exacta_Inicio_Vigencia": tramite_sasoftco['FReserva_Inicial'], # VALIDAR
                        "Nombre_CDA": tramite.id_solicitud_tramite.nombre_proyecto, # tramite_sasoftco['Npredio'] # VALIDAR
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
    
class GeoJsonPermisoEmisionesAtmosfericasView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'LA', id_permiso_ambiental__nombre__icontains = 'Permiso de emisiones atmosféricas')

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
                        "Nombre_Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Numero_Resolucion": tramite_sasoftco['Num_resolucion'], # VALIDAR
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Vigencia": "", # VALIDAR
                        "Tipo_Combustible": tramite_sasoftco['Combustible'] if tramite_sasoftco['Combustible'] != 'Otro' else tramite_sasoftco['Cual3'],
                        "Expedicion": "", # VALIDAR
                        "Latitud": tramite.coordenada_x,
                        "Longitud": tramite.coordenada_y,
                        "Nombre_Fuente": tramite.id_solicitud_tramite.nombre_proyecto, # tramite_sasoftco['Npredio'] # VALIDAR
                        "Fuente_Emision": tramite_sasoftco['Emission_source_type'] if tramite_sasoftco['Emission_source_type'] != 'Otro' else tramite_sasoftco['Cual1'],
                        "Linea_Produccion": "", # VALIDAR
                        "Produccion_Anual": "", # VALIDAR
                        "Capacidad_Instalada": "", # VALIDAR
                        "Equipo_Control": tramite_sasoftco['Equipo_Control'] if tramite_sasoftco['Equipo_Control'] != 'Otro' else tramite_sasoftco['Cual2']
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
    
class GeoJsonInscripcionAcopiadorAceitesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'RE', id_permiso_ambiental__nombre__icontains = 'Registro de Inscripción de acopiadores primarios de aceites lubricantes usados')

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
                        "Usuario": tramite.id_solicitud_tramite.id_persona_registra.user_set.all().exclude(id_usuario=1).first().nombre_de_usuario,
                        "Numero_Resolucion": "", # VALIDAR
                        "Expediente": UtilsGeoJson.get_expediente(tramite),
                        "Vigencia": "", # VALIDAR
                        "Fecha_Exacta_Inicio_Vigencia": tramite_sasoftco['FReserva_Inicial'], # VALIDAR
                        "Fecha_Expedicion_Resolucion": "", # VALIDAR
                        "Latitud": tramite.coordenada_x,
                        "Longitud": tramite.coordenada_y,
                        "Volumen_Aceite_Almacenado": tramite_sasoftco['Volac'], # VALIDAR
                        "Tipo_Acopiador": tramite_sasoftco['Tacop_value'] if tramite_sasoftco['Tacop_value'] != 'Otro' else tramite_sasoftco['Tacop2'],
                        "Tipo_Aceite_Usado": tramite_sasoftco['Toil_value'] if tramite_sasoftco['Toil_value'] != 'Otro' else tramite_sasoftco['Toil2'],
                        "Sistema_Almacenamiento_Residuos": tramite_sasoftco['Sisalm_value'] if tramite_sasoftco['Sisalm_value'] != 'Otro' else tramite_sasoftco['Sisalm2']
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