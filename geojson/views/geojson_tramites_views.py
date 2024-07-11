import json
from rest_framework.exceptions import ValidationError,NotFound,PermissionDenied
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from geojson.utils import UtilsGeoJson
from geojson.models.tramites_models import PermisosAmbSolicitudesTramite

class GeoJsonConcesionAguasSuperficialesView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        tramites = PermisosAmbSolicitudesTramite.objects.filter(id_permiso_ambiental__cod_tipo_permiso_ambiental = 'DA')

        GeoJson_list = []

        for tramite in tramites:
            tramite_sasoftco = UtilsGeoJson.get_tramite_sasoftco(tramite)

            if tramite_sasoftco:
                GeoJson = {
                    "Feature": tramite.id_permiso_ambiental.get_cod_tipo_permiso_ambiental_display(),
                    "geometry": {
                        "type": "Point",
                        "coordinates": [tramite_sasoftco['longitud'], tramite_sasoftco['latitud']]
                    },
                    "properties": {
                        "municipio": tramite.id,
                        "tipo_determinante": tramite_sasoftco['nombre'],
                        "tipo_elementos_proteccion": tramite_sasoftco['tipo'],
                        "nombre_geografico": tramite.fecha_creacion,
                        "area": tramite.estado,
                        #"latitud": tramite_sasoftco['latitud'],
                        #"longitud": tramite_sasoftco['longitud'],
                        "expediente": tramite_sasoftco['NumExp'],
                        "usuario": tramite.id_usuario.username,
                        "resolucion": tramite_sasoftco['NumResol'],
                        "fecha_resolucion": tramite_sasoftco['Fecha_Resolu'],
                        "estado": tramite.id_permiso_ambiental.estado,
                    }
                }
                GeoJson_list.append(GeoJson)

        return Response(GeoJson_list)