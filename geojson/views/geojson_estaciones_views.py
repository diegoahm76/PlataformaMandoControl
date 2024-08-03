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
import datetime

class GeoJsonEstacionesView(generics.ListAPIView):
    def get(self, request):
        estaciones = Estaciones.objects.all().order_by("id_estacion").using("bia-estaciones")
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
            activo = False
            if datos_estacion.fecha_registro is not None:
                fecha_registro = datos_estacion.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
                fecha_hoy = datetime.datetime.now() - datetime.timedelta(minutes=10)
                if fecha_registro > fecha_hoy:
                    activo = True
            
            GeoJson = {
                "type": "Feature",
                "id": estacion.id_estacion,
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(estacion.longitud), float(estacion.latitud)]
                },
                "properties": {
                    "id_estacion": estacion.id_estacion,
                    "nombre_estacion": estacion.nombre_estacion,
                    "cod_tipo_estacion": estacion.cod_tipo_estacion,
                    "cod_municipio": estacion.cod_municipio if estacion.cod_municipio is not None else " ",
                    "indicaciones_ubicacion": estacion.indicaciones_ubicacion if estacion.indicaciones_ubicacion is not None else " ",
                    "fecha_modificacion": estacion.fecha_modificacion if estacion.fecha_modificacion is not None else " ",
                    "fecha_modificacion_coordenadas": estacion.fecha_modificacion_coordenadas if estacion.fecha_modificacion_coordenadas is not None else " ",
                    "id_persona_modifica": estacion.id_persona_modifica if estacion.id_persona_modifica is not None else " ",
                    "activo": activo,
                    "nombre_persona_modifica": nombre_persona if nombre_persona is not None else " ",
                    "fecha_registro": datos_estacion.fecha_registro if datos_estacion is not None else " ",
                    "temperatura_ambiente": f'{datos_estacion.temperatura_ambiente} °C' if datos_estacion is not None else "0.00 °C",
                    "humedad_ambiente": f'{datos_estacion.humedad_ambiente} %' if datos_estacion is not None else "0.00 %",
                    "presion_barometrica": f'{datos_estacion.presion_barometrica} hPa' if datos_estacion is not None else "0.00 hPa",
                    "velocidad_viento": f'{datos_estacion.velocidad_viento} m/s' if datos_estacion is not None else "0.00 m/s",
                    "direccion_viento": f'{datos_estacion.direccion_viento}°' if datos_estacion is not None else "0.00°",
                    "precipitacion": f'{datos_estacion.precipitacion} mm' if datos_estacion is not None else "0.00 mm",
                    "luminosidad": f'{datos_estacion.luminosidad} Lux' if datos_estacion is not None else "0.00 Lux",
                    "nivel_agua": f'{datos_estacion.nivel_agua} m' if datos_estacion is not None else "0.00 m",
                    "velocidad_agua": f'{datos_estacion.velocidad_agua} m/s' if datos_estacion is not None else "0.00 m/s",
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
    

class GeoJsonEstacionesViewDetail(generics.RetrieveAPIView):
    def get(self, request):

        datos_all = Datos.objects.all().order_by("id_estacion", "-fecha_registro").using("bia-estaciones")

        GeoJson_list = []

        for datos in datos_all:
            GeoJson = {
            "type": "Feature",
            "id": datos.id_data,
            "geometry": {
                "type": "Point",
                "coordinates": [float(datos.id_estacion.longitud), float(datos.id_estacion.latitud)]
            },
            "properties": {
                "id_estacion": datos.id_estacion.id_estacion,
                "fecha_registro": datos.fecha_registro if datos is not None else " ",
                "temperatura_ambiente": f'{datos.temperatura_ambiente} °C' if datos.temperatura_ambiente is not None else "0.00 °C",
                "humedad_ambiente": f'{datos.humedad_ambiente} %' if datos.humedad_ambiente is not None else "0.00 %",
                "presion_barometrica": f'{datos.presion_barometrica} hPa' if datos.presion_barometrica is not None else "0.00 hPa",
                "velocidad_viento": f'{datos.velocidad_viento} m/s' if datos.velocidad_viento is not None else "0.00 m/s",
                "direccion_viento": f'{datos.direccion_viento}°' if datos.direccion_viento is not None else "0.00°",
                "precipitacion": f'{datos.precipitacion} mm' if datos.precipitacion is not None else "0.00 mm",
                "luminosidad": f'{datos.luminosidad} Lux' if datos.luminosidad is not None else "0.00 Lux",
                "nivel_agua": f'{datos.nivel_agua} m' if datos.nivel_agua is not None else "0.00 m",
                "velocidad_agua": f'{datos.velocidad_agua} m/s' if datos.velocidad_agua is not None else "0.00 m/s",
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
   

