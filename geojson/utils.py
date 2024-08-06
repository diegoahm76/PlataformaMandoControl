from datetime import datetime
import json

from geojson.models.radicados_models import ConfigTiposRadicadoAgno
from geojson.models.tramites_models import Tramites
from rest_framework.exceptions import NotFound
import json, random, requests
from shapely.geometry import shape, Point
from pyproj import Proj

class UtilsGeoJson:
    @staticmethod
    def get_tramite_sasoftco(tramite):
        cadena = ""
        radicado = tramite.id_solicitud_tramite.id_radicado
        organized_data = {}
        if radicado:
            instance_config_tipo_radicado = ConfigTiposRadicadoAgno.objects.filter(agno_radicado=radicado.agno_radicado,cod_tipo_radicado=radicado.cod_tipo_radicado).first()
            numero_con_ceros = str(radicado.nro_radicado).zfill(instance_config_tipo_radicado.cantidad_digitos)
            cadena= instance_config_tipo_radicado.prefijo_consecutivo+'-'+str(instance_config_tipo_radicado.agno_radicado)+'-'+numero_con_ceros

            tramites_values = Tramites.objects.filter(radicate_bia=cadena).values()

                
            if tramites_values:
                organized_data = {
                    'procedure_id': tramites_values[0]['procedure_id'],
                    'radicate_bia': tramites_values[0]['radicate_bia'],
                    'proceeding_id': tramites_values[0]['proceeding_id'],
                }
                
                for item in tramites_values:
                    field_name = item['name_key']
                    if item['type_key'] == 'json':
                        value = json.loads(item['value_key'])
                    else:
                        value = item['value_key']
                    organized_data[field_name] = value
            else:
                raise NotFound('No se encontró el detalle del trámite elegido')
            
        return organized_data
    
    @staticmethod
    def get_nombre_persona(persona):
        nombre_completo_persona = ""
        if persona.tipo_persona == 'J':
            nombre_completo_persona = persona.razon_social
        else:
            nombre_list = [persona.primer_nombre, persona.segundo_nombre,
                            persona.primer_apellido, persona.segundo_apellido]
            nombre_completo_persona = ' '.join(item for item in nombre_list if item is not None)
            nombre_completo_persona = nombre_completo_persona if nombre_completo_persona != "" else None
            
        return nombre_completo_persona
    
    @staticmethod
    def get_expediente(tramite):
        expediente = ""
        if tramite.id_solicitud_tramite.id_expediente:
            expediente = f"{tramite.id_solicitud_tramite.id_expediente.codigo_exp_und_serie_subserie}-{tramite.id_solicitud_tramite.id_expediente.codigo_exp_Agno}-{tramite.id_solicitud_tramite.id_expediente.codigo_exp_consec_por_agno}"
        return expediente
    
    @staticmethod
    def random_point_in_country(country_name: str) -> tuple:
        url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
        try:
            response = requests.get(url)
            if response.status_code == 200:

                data = json.loads(response.text)
                country = [country for country in data["features"] if country["properties"]["name"] in country_name][0]

                feature = shape(country["geometry"])
                minx, miny, maxx, maxy = feature.bounds

                while True:
                    pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
                    if feature.contains(pnt):
                        return float(pnt.y), float(pnt.x)

        except Exception as e:
            return 0, 0
    
    @staticmethod
    def transform_coordinates(lat, lon) -> tuple:
        p = Proj('+proj=tmerc +lat_0=4.0 +lon_0=-73.0 +k=0.9992 +x_0=5000000 +y_0=2000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
        lon_final, lat_final = p(lon,lat)

        return lat_final, lon_final
        
    @staticmethod
    def get_coordinates(lat, lon, nacional=False) -> tuple:
        lat_final = 0
        lon_final = 0

        if (not lat or not lon) or (lat == '' or lon == ''):
            lat_final, lon_final  = UtilsGeoJson.random_point_in_country("Colombia")

            # CONVERTIR A COORDENADAS NACIONALES
            if nacional:
                lat_final, lon_final  = UtilsGeoJson.transform_coordinates(lat_final, lon_final)
        else:
            if isinstance(lat, str) or isinstance(lon, str):
                if lat.isdigit() or lon.isdigit():
                    lat_final, lon_final  = UtilsGeoJson.random_point_in_country("Colombia")

                    # CONVERTIR A COORDENADAS NACIONALES
                    if nacional:
                        lat_final, lon_final  = UtilsGeoJson.transform_coordinates(lat_final, lon_final)
                else:
                    lat_final = float(lat)
                    lon_final = float(lon)
            else:
                lat_final = float(lat)
                lon_final = float(lon)

        return lat_final, lon_final
        