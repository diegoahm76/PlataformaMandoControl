from django.urls import path
from geojson.views import geojson_estaciones_views as estaciones_views
from geojson.views import geojson_tramites_views as tramites_views
from geojson.views import geojson_opas_views as opas_views
from geojson.views import geojson_permisosmenores_views as permisosmenores_views

urlpatterns=[

    #Tramites
    path('tramite/DM/get/',tramites_views.GeoJsonDeterminantesAmbientalesView.as_view(),name='geojson-determinantes-ambientales'),
    path('tramite/CE/get/',tramites_views.GeoJsonCertificacionAmbientalDesintegracionVehicularView.as_view(),name='geojson-certificacion-ambiental-desintegracion-vehicular'),

    #Opas
    path('opa/inscripcion_dga/get/',opas_views.GeoJsonInscripcionDGAView.as_view(),name='geojson-inscripcion-dga'),
    path('opa/formulacion_proyectos_escolares/get/',opas_views.GeoJsonFormulacionProyectosEscolaresView.as_view(),name='geojson-formulacion-proyectos-escolares'),


    #Estaciones
    path('estaciones/get/',estaciones_views.GeoJsonEstacionesView.as_view(),name='geojson-estaciones'),

    #Permisos Menores
    path('PM/Certificacion_inscripcion_control/get/',permisosmenores_views.GeoJsonCertificacionInscripcionControlView.as_view(),name='geojson-certificacion-inscripcion-control'),
]