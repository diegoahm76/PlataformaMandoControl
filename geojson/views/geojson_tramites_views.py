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