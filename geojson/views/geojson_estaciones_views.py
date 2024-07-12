import json
from seguridad.utils import Util
from rest_framework.exceptions import ValidationError,NotFound,PermissionDenied
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from geojson.utils import UtilsGeoJson
from geojson.models.tramites_models import SolicitudesTramites, PermisosAmbientales, PermisosAmbSolicitudesTramite
from geojson.models.estaciones_models import Estaciones, Datos
from geojson.models.personas_models import Personas

class GeoJsonEstacionesView(generics.ListAPIView):
    def get(self, request):
        estaciones = Estaciones.objects.all().using("bia-estaciones")
        datos = Datos.objects.all().order_by("-fecha_registro").using("bia-estaciones")
        persona = Personas.objects.all()

        GeoJson_list = []

        for estacion in estaciones:
            datos_estacion = datos.filter(id_estacion=estacion.id_estacion).first()
            nombre_persona = None
            if estacion.id_persona_modifica is not None:
                try:
                    persona_modifica = persona.get(id_persona=estacion.id_persona_modifica)
                except:
                    persona_modifica = None
                if persona_modifica is not None:
                    nombre_persona = ' '.join(filter(None, [persona_modifica.primer_nombre, persona_modifica.segundo_nombre, persona_modifica.primer_apellido, persona_modifica.segundo_apellido]))
                
            if datos_estacion is not None:
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
                        "nombre_persona_modifica": nombre_persona,
                        "fecha_registro": datos_estacion.fecha_registro,
                        "temperatura_ambiente": datos_estacion.temperatura_ambiente,
                        "humedad_ambiente": datos_estacion.humedad_ambiente,
                        "presion_barometrica": datos_estacion.presion_barometrica,
                        "velocidad_viento": datos_estacion.velocidad_viento,
                        "direccion_viento": datos_estacion.direccion_viento,
                        "precipitacion": datos_estacion.precipitacion,
                        "luminosidad": datos_estacion.luminosidad,
                        "nivel_agua": datos_estacion.nivel_agua,
                        "velocidad_agua": datos_estacion.velocidad_agua,
                    }
                }
                GeoJson_list.append(GeoJson)
            else:
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
                        "nombre_persona_modifica": nombre_persona,
                    }
                }
                GeoJson_list.append(GeoJson)

        return Response({
            "type": "FeatureCollection",
            "features": GeoJson_list
        })
