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
    path('tramite/permiso_ocupacion_playa/get/',tramites_views.GeoJsonPermisoOcupacionPlayaView.as_view(),name='geojson-permiso-ocupacion-playa'),
    path('tramite/aprovechamiento_carbon_vegetal/get/',tramites_views.GeoJsonAprovechamientoCarbonVegetalMovilizacionView.as_view(),name='geojson-aprovechamiento-carbon-vegetal'),
    path('tramite/aprovechamiento_ambiental_productos_f/get/',tramites_views.GeoJsonAprovechamientoProductosForestalesView.as_view(),name='geojson-aprovechamiento-ambiental-productos-f'), 
    path('tramite/permiso_vertimientos_agua/get/',tramites_views.GeoJsonPermisoVertimientosAguaView.as_view(),name='geojson-permiso-vertimientos-agua'),
    path('tramite/permiso_vertimientos_suelo/get/',tramites_views.GeoJsonPermisoVertimientosSueloView.as_view(),name='geojson-permiso-vertimientos-agua'),
    path('tramite/permiso_prospeccion_aguas_subterraneas/get/',tramites_views.GeoJsonPermisosProspeccionAguasSubterraneasView.as_view(),name='geojson-permiso-prospeccion-agua'),
    path('tramite/planes_contingencia_estaciones_servicio/get/',tramites_views.GeoJsonPlanesContingenciaEstacionesServicioView.as_view(),name='geojson-planes-contingencia-estaciones-servicio'),
    path('tramite/proyectos_industriales_minerias/get/',tramites_views.GeoJsonProyectosIndustrialesMineriasView.as_view(),name='geojson-proyectos-industriales-minerias'),
    path('tramite/permiso_ocupacion_cauces/get/',tramites_views.GeoJsonPermisoOcupacionCaucesView.as_view(),name='geojson-permiso-ocupacion-cauces'),
    path('tramite/recoleccion_especimenes/get/',tramites_views.GeoJsonRecoleccionEspecimenesView.as_view(),name='geojson-recoleccion-especimenes'),
    path('tramite/certificacion_ambiental_automotores/get/',tramites_views.GeoJsonCertificacionAmbientalAutomotoresView.as_view(),name='geojson-certificacion-ambiental-automotores'),
    path('tramite/permiso_emisiones_atmosfericas/get/',tramites_views.GeoJsonPermisoEmisionesAtmosfericasView.as_view(),name='geojson-permiso-emisiones-atmosfericas'),
    path('tramite/inscripcion_acopiador_aceites/get/',tramites_views.GeoJsonInscripcionAcopiadorAceitesView.as_view(),name='geojson-inscripcion-acopiador-aceites'),
    path('tramite/reporte_vivero/get/',tramites_views.GeoJsonReporteViveroView.as_view(),name='geojson-reporte-vivero'),
    path('tramite/almacenamiento_sustancias_nocivas/get/',tramites_views.GeoJsonAlmacenamientoSustanciasNocivasView.as_view(),name='geojson-almacenamiento-sustancias-nocivas'),
    path('tramite/registro_libro_operaciones/get/',tramites_views.GeoJsonRegistroLibroOperacionesView.as_view(),name='geojson-registro-libro-operaciones'),
    # path('tramite/pqrsdf/get/',tramites_views.GeoJsonPQRSDFView.as_view(),name='geojson-pqrsdf'),

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