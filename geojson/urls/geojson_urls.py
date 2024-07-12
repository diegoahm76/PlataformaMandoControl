from django.urls import path
from geojson.views import geojson_estaciones_views as estaciones_views
from geojson.views import geojson_tramites_views as tramites_views
from geojson.views import geojson_opas_views as opas_views

urlpatterns=[

    #Tramites
    path('tramite/DM/get/',tramites_views.GeoJsonDeterminantesAmbientalesView.as_view(),name='geojson-determinantes-ambientales'),

    #Opas
    path('opa/inscripcion_dga/get/',opas_views.GeoJsonInscripcionDGAView.as_view(),name='geojson-inscripcion-dga'),
    path('opa/formulacion_proyectos_escolares/get/',opas_views.GeoJsonFormulacionProyectosEscolaresView.as_view(),name='geojson-formulacion-proyectos-escolares'),


    #Estaciones
    path('estaciones/get/',estaciones_views.GeoJsonEstacionesView.as_view(),name='geojson-estaciones'),
]