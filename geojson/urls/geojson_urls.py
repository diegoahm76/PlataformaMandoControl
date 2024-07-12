from django.urls import path
from geojson.views import geojson_estaciones_views as estaciones_views
from geojson.views import geojson_tramites_views as tramites_views
from geojson.views import geojson_opas_views as opas_views

urlpatterns=[
    #Estaciones

    #Tramites
    path('tramite/conc_aguas/get/',tramites_views.GeoJsonConcesionAguasSuperficialesView.as_view(),name='geojson-concesion-aguas'),

    #Opas
    path('opa/inscripcion_dga/get/',opas_views.GeoJsonInscripcionDGAView.as_view(),name='geojson-inscripcion-dga'),

    #Estaciones
    path('estaciones/get/',estaciones_views.GeoJsonEstacionesView.as_view(),name='geojson-estaciones'),
]