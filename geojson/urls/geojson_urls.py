from django.urls import path
from geojson.views import geojson_estaciones_views as estaciones_views
from geojson.views import geojson_tramites_views as tramites_views

urlpatterns=[
    #Estaciones

    #Tramites
    path('tramite/conc_aguas/get/',tramites_views.GeoJsonConcesionAguasSuperficialesView.as_view(),name='geojson-concesion-aguas'),
]