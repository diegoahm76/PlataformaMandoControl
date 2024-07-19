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
    path('tramite/permiso_vertimientos_agua/get/',tramites_views.GeoJsonPermisoVertimientosAguaView.as_view(),name='geojson-permiso-vertimientos-agua'),
    path('tramite/permiso_vertimientos_suelo/get/',tramites_views.GeoJsonPermisoVertimientosSueloView.as_view(),name='geojson-permiso-vertimientos-agua'),

    #Opas
    path('opa/inscripcion_dga/get/',opas_views.GeoJsonInscripcionDGAView.as_view(),name='geojson-inscripcion-dga'),
    path('opa/inscripcion_generador_rcd/get/',opas_views.GeoJsonInscripcionGeneradorRCDView.as_view(),name='geojson-inscripcion-generador-rcd'),
    path('opa/inscripcion_generador_acu/get/',opas_views.GeoJsonInscripcionGeneradorACUView.as_view(),name='geojson-inscripcion-generador-acu'),
    path('opa/inscripcion_gestion_acu/get/',opas_views.GeoJsonInscripcionGestionACUView.as_view(),name='geojson-inscripcion-gestion-acu'),
    path('opa/formulacion_proyectos_escolares/get/',opas_views.GeoJsonFormulacionProyectosEscolaresView.as_view(),name='geojson-formulacion-proyectos-escolares'),
    path('opa/inscripcion_generador_residuos/get/',opas_views.GeoJsonInscripcionGeneradorResiduosView.as_view(),name='geojson-inscripcion-generador-residuos'),
    path('opa/registro_inventario_nacional/get/',opas_views.GeoJsonRegistroInventarioNacionalView.as_view(),name='geojson-registro-inventario-nacional'),
    path('opa/registro_unico_ambiental_RUA/get/',opas_views.GeoJsonRegistroUnicoAmbientalRUAView.as_view(),name='geojson-registro-unico-ambiental-RUA'),
    path('opa/salvoconducto_movilizacion/get/',opas_views.GeoJsonSalvoconductoMovilizacionEspecimenesView.as_view(),name='geojson-salvoconducto-movilizacion'),
    path('opa/negocios_verdes/get/',opas_views.GeoJsonNegociosVerdesView.as_view(),name='geojson-negocios-verdes'),
    path('opa/planes_paisajisticos_ordenato/get/',opas_views.GeoJsonPlanesPaisajisticosOrdenatoView.as_view(),name='geojson-planes-paisajisticos-ordenato'),



    #Estaciones
    path('estaciones/get/',estaciones_views.GeoJsonEstacionesView.as_view(),name='geojson-estaciones'),
    path('estaciones/datos/get/',estaciones_views.GeoJsonEstacionesViewDetail.as_view(),name='geojson-estaciones-datos'),

    #Permisos Menores
    path('PM/Certificacion_inscripcion_control/get/',permisosmenores_views.GeoJsonCertificacionInscripcionControlView.as_view(),name='geojson-certificacion-inscripcion-control'),
    path('PM/permiso_caza/get/',permisosmenores_views.GeoJsonPermisoCazaView.as_view(),name='geojson-permiso-caza'),
    path('PM/red_amigos_silvestres/get/',permisosmenores_views.GeoJsonRedAmigosSilvestresView.as_view(),name='geojson-red-amigos-silvestres'),
    path('PM/registro_plantaciones_forestales/get/',permisosmenores_views.GeoJsonRegistroPlantacionesForestales.as_view(),name='geojson-registro-plantaciones-forestales'),
    path('PM/licencia_establecimiento_zoocriadero/get/',permisosmenores_views.GeoJsonRegistroLicenciaZoocriadero.as_view(),name='geojson-licencia-establecimiento-zoocriadero'),
    path('PM/permiso_zoologico/get/',permisosmenores_views.GeoJsonPermisoZoologico.as_view(),name='geojson-permiso-zoologico'),


    
]