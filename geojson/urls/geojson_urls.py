from django.urls import path
from geojson.views import geojson_estaciones_views as estaciones_views
from geojson.views import geojson_tramites_views as tramites_views
from geojson.views import geojson_opas_views as opas_views

urlpatterns=[

    #Tramites
    path('tramite/DM/get/',tramites_views.GeoJsonDeterminantesAmbientalesView.as_view(),name='geojson-determinantes-ambientales'),
    path('tramite/inscripcion_gestor_rcd/get/',tramites_views.GeoJsonInscripcionGestorRCDView.as_view(),name='geojson-inscripcion-generador-rcd'),
    path('tramite/licencia_ambiental_transferencia_electrica/get/',tramites_views.GeoJsonLicenciaAmbientalTransElectricaView.as_view(),name='geojson-licencia-ambiental-transferencia-eléctrica'),
    path('tramite/permiso_ocupación_cauce_playa_y_lechos/get/',tramites_views.GeoJsonPermisoOcupacionCaucePlayaLechosView.as_view(),name='geojson-permiso-ocupación-cauce-playa-y-lechos'),

    #Opas
    path('opa/inscripcion_dga/get/',opas_views.GeoJsonInscripcionDGAView.as_view(),name='geojson-inscripcion-dga'),
    path('opa/inscripcion_generador_rcd/get/',opas_views.GeoJsonInscripcionGeneradorRCDView.as_view(),name='geojson-inscripcion-generador-rcd'),
    path('opa/inscripcion_generador_acu/get/',opas_views.GeoJsonInscripcionGeneradorACUView.as_view(),name='geojson-inscripcion-generador-acu'),
    path('opa/formulacion_proyectos_escolares/get/',opas_views.GeoJsonFormulacionProyectosEscolaresView.as_view(),name='geojson-formulacion-proyectos-escolares'),


    #Estaciones
    path('estaciones/get/',estaciones_views.GeoJsonEstacionesView.as_view(),name='geojson-estaciones'),
]