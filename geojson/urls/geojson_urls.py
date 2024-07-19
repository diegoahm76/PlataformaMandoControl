from django.urls import path
from geojson.views import geojson_estaciones_views as estaciones_views
from geojson.views import geojson_tramites_views as tramites_views
from geojson.views import geojson_opas_views as opas_views
from geojson.views import geojson_permisosmenores_views as permisosmenores_views

urlpatterns=[

    #Tramites
    path('tramite/DM/get/',tramites_views.GeoJsonDeterminantesAmbientalesView.as_view(),name='geojson-determinantes-ambientales'),
    path('tramite/CE/get/',tramites_views.GeoJsonCertificacionAmbientalDesintegracionVehicularView.as_view(),name='geojson-certificacion-ambiental-desintegracion-vehicular'),
    path('tramite/inscripcion_gestor_rcd/get/',tramites_views.GeoJsonInscripcionGestorRCDView.as_view(),name='geojson-inscripcion-generador-rcd'),
    path('tramite/licencia_ambiental_transferencia_electrica/get/',tramites_views.GeoJsonLicenciaAmbientalTransElectricaView.as_view(),name='geojson-licencia-ambiental-transferencia-eléctrica'),
    path('tramite/permiso_ocupación_cauce_playa_y_lechos/get/',tramites_views.GeoJsonPermisoOcupacionCaucePlayaLechosView.as_view(),name='geojson-permiso-ocupación-cauce-playa-y-lechos'),
    path('tramite/aprovechamiento_carbon_vegetal/get/',tramites_views.GeoJsonAprovechamientoCarbonVegetalMovilizacionView.as_view(),name='geojson-aprovechamiento-carbon-vegetal'),
    path('tramite/aprovechamiento_ambiental_productos_f/get/',tramites_views.GeoJsonAprovechamientoProductosForestalesView.as_view(),name='geojson-aprovechamiento-ambiental-productos-f'), 

    #Opas
    path('opa/inscripcion_dga/get/',opas_views.GeoJsonInscripcionDGAView.as_view(),name='geojson-inscripcion-dga'),
    path('opa/inscripcion_generador_rcd/get/',opas_views.GeoJsonInscripcionGeneradorRCDView.as_view(),name='geojson-inscripcion-generador-rcd'),
    path('opa/inscripcion_generador_acu/get/',opas_views.GeoJsonInscripcionGeneradorACUView.as_view(),name='geojson-inscripcion-generador-acu'),
    path('opa/inscripcion_gestion_acu/get/',opas_views.GeoJsonInscripcionGestionACUView.as_view(),name='geojson-inscripcion-gestion-acu'),
    path('opa/formulacion_proyectos_escolares/get/',opas_views.GeoJsonFormulacionProyectosEscolaresView.as_view(),name='geojson-formulacion-proyectos-escolares'),


    #Estaciones
    path('estaciones/get/',estaciones_views.GeoJsonEstacionesView.as_view(),name='geojson-estaciones'),

    #Permisos Menores
    path('PM/Certificacion_inscripcion_control/get/',permisosmenores_views.GeoJsonCertificacionInscripcionControlView.as_view(),name='geojson-certificacion-inscripcion-control'),
    path('estaciones-datos/get/',estaciones_views.GeoJsonEstacionesViewDetail.as_view(),name='geojson-estaciones-datos'),
]