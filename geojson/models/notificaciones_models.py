from django.db import models
from geojson.choices.tipo_soli_noti_choices import tipo_soli_noti_CHOICES
from geojson.choices.pqrsdf_choices import RELACION_TITULAR
from geojson.choices.cod_medio_solicitud_choices import cod_medio_solicitud_CHOICES
from geojson.choices.cod_estado_noti_choices import cod_estado_noti_CHOICES
from geojson.choices.estado_asignacion_choices import ESTADO_ASIGNACION_CHOICES
from geojson.models.expedientes_models import DocumentosDeArchivoExpediente, ExpedientesDocumentales
from geojson.models.base_models import Municipio
from geojson.models.organigrama_models import UnidadesOrganizacionales


class NotificacionesCorrespondencia(models.Model):
    id_notificacion_correspondencia = models.SmallAutoField(primary_key=True, db_column='T350IdNotificacionCorrespondencia')
    cod_tipo_solicitud = models.CharField(choices=tipo_soli_noti_CHOICES, max_length=2, db_column='T350codTipoSolicitud')
    cod_tipo_documento = models.ForeignKey('TiposDocumentos', on_delete=models.CASCADE, db_column='T350codTipoDocumento',related_name='T350codTipoDocumento')
    id_PQRSDF = models.ForeignKey('geojson.PQRSDF', on_delete=models.SET_NULL, null=True, blank=True, db_column='T350Id_PQRSDF',related_name='T350IdPQRSDF')
    id_expediente_documental = models.ForeignKey(ExpedientesDocumentales, on_delete=models.SET_NULL, null=True, blank=True, db_column='T350Id_ExpedienteDocumental', related_name='T350IdExpedienteDocumental')
    id_solicitud_tramite = models.ForeignKey('geojson.SolicitudesTramites', on_delete=models.SET_NULL, null=True, blank=True, db_column='T350Id_SolicitudTramite',related_name='T350IdSolicitudTramite')
    id_acto_administrativo = models.ForeignKey('geojson.ActosAdministrativos', on_delete=models.SET_NULL, null=True, blank=True, db_column='T350Id_ActoAdministrativo',related_name='T350IdActoAdministrativo')
    procede_recurso_reposicion = models.BooleanField(null=True, db_column='T350procedeRecursoReposicion')
    id_persona_titular = models.ForeignKey('geojson.Personas', on_delete=models.SET_NULL, null=True, blank=True, db_column='T350Id_PersonaTitular',related_name='T350IdPersonaTitular')
    id_persona_interpone = models.ForeignKey('geojson.Personas', on_delete=models.SET_NULL, null=True, blank=True, db_column='T350Id_PersonaInterpone',related_name='T350IdPersonaInterpone')
    cod_relacion_con_titular = models.CharField(choices=RELACION_TITULAR, max_length=2, null=True, db_column='T350codRelacionConTitular')
    es_anonima = models.BooleanField(null=True, db_column='T350esAnonima')
    permite_notificacion_email = models.BooleanField(null=True, db_column='T350permiteNotificacionEmail')
    persona_a_quien_se_dirige = models.CharField(max_length=255, null=True, db_column='T350personaAQuienSeDirige')
    cod_tipo_documentoID = models.ForeignKey('geojson.TipoDocumento', on_delete=models.CASCADE, db_column='T350codTipoDocumentoID',related_name='T350codTipoDocumentoID')
    nro_documentoID = models.CharField(max_length=20, db_column='T350nroDocumentoID')
    cod_municipio_notificacion_nal = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, db_column='T350codMunicipioNotificacionNal',related_name='T350codMunicipioNotificacionNal')
    dir_notificacion_nal = models.CharField(max_length=255, null=True, db_column='T350dirNotificacionNal')
    tel_celular = models.CharField(max_length=15, null=True, db_column='T350telCelular')
    tel_fijo = models.CharField(max_length=15, null=True, db_column='T350telFijo')
    email_notificacion = models.CharField(max_length=100, null=True, db_column='T350emailNotificacion')
    asunto = models.CharField(max_length=100, db_column='T350asunto')
    descripcion = models.CharField(max_length=500, null=True, db_column='T350descripcion')
    cod_medio_solicitud = models.CharField(choices=cod_medio_solicitud_CHOICES, max_length=2, db_column='T350codMedioSolicitud')
    fecha_solicitud = models.DateTimeField(db_column='T350fechaSolicitud')
    id_persona_solicita = models.ForeignKey('geojson.Personas', on_delete=models.CASCADE, db_column='T350Id_PersonaSolicita',related_name='T350IdPersonaSolicita')
    id_und_org_oficina_solicita = models.ForeignKey(UnidadesOrganizacionales, on_delete=models.CASCADE, db_column='T350Id_UndOrgOficinaSolicita',related_name='T350IdUndOrgOficinaSolicita')
    allega_copia_fisica = models.BooleanField(null=True, db_column='T350allegaCopiaFisica')
    cantidad_anexos = models.SmallIntegerField(null=True, db_column='T350cantidadAnexos')
    nro_folios_totales = models.SmallIntegerField(null=True, db_column='T350nroFoliosTotales')
    id_persona_recibe_solicitud_manual = models.ForeignKey('geojson.Personas', on_delete=models.SET_NULL, null=True, blank=True, db_column='T350Id_PersonaRecibeSolicitudManual',related_name='T350IdPersonaRecibeSolicitudManual')
    id_persona_asigna = models.ForeignKey('geojson.Personas', on_delete=models.SET_NULL, null=True, blank=True, db_column='T350Id_PersonaAsigna',related_name='T350IdPersonaAsigna')
    id_persona_asignada = models.ForeignKey('geojson.Personas', on_delete=models.SET_NULL, null=True, blank=True, db_column='T350Id_PersonaAsignada',related_name='T350IdPersonaAsignada')
    cod_estado_asignacion = models.CharField(choices=ESTADO_ASIGNACION_CHOICES, max_length=2, null=True, db_column='T350codEstadoAsignacion')
    fecha_eleccion_estado = models.DateTimeField(null=True, db_column='T350fechaEleccionEstado')
    justificacion_rechazo_asignacion = models.CharField(max_length=250, null=True, db_column='T350justificacionRechazoAsignacion')
    requiere_digitalizacion = models.BooleanField(null=True, db_column='T350requiereDigitalizacion')
    fecha_envio_definitivo_a_digitalizacion = models.DateTimeField(null=True, db_column='T350fechaEnvioDefinitivoADigitalizacion')
    fecha_digitalizacion_completada = models.DateTimeField(null=True, db_column='T350fechaDigitalizacionCompletada')
    ya_digitizado = models.BooleanField(null=True, db_column='T350yaDigitizado')
    fecha_rta_final_gestion = models.DateTimeField(null=True, db_column='T350fechaRtaFinalGestion')
    id_persona_rta_final_gestion = models.ForeignKey('geojson.Personas', on_delete=models.SET_NULL, null=True, blank=True, db_column='T350Id_PersonaRtaFinalGestion',related_name='T350IdPersonaRtaFinalGestion')
    solicitud_aceptada_rechazada = models.BooleanField(null=True, db_column='T350solicitudAceptadaRechazada')
    fecha_devolucion = models.DateTimeField(null=True, db_column='T350fechaDevolucion')
    justificacion_rechazo = models.CharField(max_length=250, null=True, db_column='T350justificacionRechazo')
    cod_estado = models.CharField(choices=cod_estado_noti_CHOICES, max_length=2, db_column='T350codEstado')
    id_doc_de_arch_exp = models.ForeignKey(DocumentosDeArchivoExpediente, on_delete=models.SET_NULL, null=True, blank=True, db_column='T350Id_DocDeArchExp',related_name='T350IdDocDeArchExp')

    class Meta:
        db_table = 'T350NotificacionesCorrespondencia'

class TiposDocumentos(models.Model):
    id_tipo_documento = models.SmallAutoField(primary_key=True, db_column='T359IdTipoDocumento')
    nombre = models.CharField(max_length=255, db_column='T359nombre')
    aplica_para_notificaciones = models.BooleanField(db_column='T359aplicaParaNotificaciones')
    aplica_para_correspondencia = models.BooleanField(db_column='T359aplicaParaCorrespondencia')
    aplica_para_publicaciones = models.BooleanField(db_column='T359aplicaParaPublicaciones', null=True, blank=True)
    aplica_para_comunicaciones = models.BooleanField(db_column='T359aplicaParaComunicaciones', null=True, blank=True)
    aplica_para_notificaciones_publicaciones = models.BooleanField(db_column='T359aplicaParaNotificacionesPublicaciones', null=True, blank=True)
    registro_precargado = models.BooleanField(db_column='T359registroPrecargado')
    activo = models.BooleanField(db_column='T359activo')
    item_ya_usado = models.BooleanField(db_column='T359itemYaUsado')

    class Meta:
        db_table = 'T359TiposDocumentos'