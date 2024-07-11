from django.db import models
from geojson.choices.pqrsdf_choices import (
    TIPOS_OFICIO_CHOICES,
    TIPOS_PQR,
    RELACION_TITULAR,
    FORMA_PRESENTACION
    
)

from geojson.models.expedientes_models import ArchivosDigitales, DocumentosDeArchivoExpediente, ExpedientesDocumentales
from geojson.models.trd_models import TipologiasDoc
from geojson.choices.tipo_radicado_choices import TIPOS_RADICADO_CHOICES
from geojson.models.base_models import Municipio
from geojson.models.entidades_models import SucursalesEmpresas
from geojson.models.organigrama_models import UnidadesOrganizacionales
from geojson.choices.medio_almacenamiento_choices import medio_almacenamiento_CHOICES
from geojson.choices.tipo_archivo_choices import tipo_archivo_CHOICES
from geojson.choices.origen_archivo_choices import origen_archivo_CHOICES
from geojson.choices.codigo_relacion_titular_choices import cod_relacion_persona_titular_CHOICES
from geojson.choices.codigo_forma_presentacion_choices import cod_forma_presentacion_CHOICES

class ConfigTiposRadicadoAgno(models.Model):

    id_config_tipo_radicado_agno = models.SmallAutoField(primary_key=True, db_column='T235IdConfigTipoRadicadoAgno')
    agno_radicado = models.SmallIntegerField(db_column='T235agnoRadicado')
    cod_tipo_radicado = models.CharField(max_length=1, choices=TIPOS_RADICADO_CHOICES, db_column='T235codTipoRadicado')
    prefijo_consecutivo = models.CharField(null=True,max_length=10, db_column='T235prefijoConsecutivo')
    consecutivo_inicial = models.IntegerField(null=True,db_column='T235consecutivoInicial')
    cantidad_digitos = models.SmallIntegerField(null=True,db_column='T235cantidadDigitos')
    implementar = models.BooleanField(db_column='T235implementar')
    id_persona_config_implementacion = models.ForeignKey('geojson.Personas',null=True, on_delete=models.CASCADE, db_column='T235Id_PersonaConfigImplementacion',related_name='T235Id_PersonaConfigImplementacion')
    fecha_inicial_config_implementacion = models.DateTimeField(null=True,db_column='T235fechaInicialConfigImplementacion')
    consecutivo_actual = models.IntegerField(null=True,db_column='T235consecutivoActual')
    fecha_consecutivo_actual = models.DateTimeField(null=True,db_column='T235fechaConsecutivoActual')
    id_persona_consecutivo_actual = models.ForeignKey('geojson.Personas',null=True, on_delete=models.CASCADE, db_column='T235Id_PersonaConsecutivoActual',related_name='FK2_T235ConfigTiposRadicadoAgno')

    class Meta:
        db_table = 'T235ConfigTiposRadicadoAgno'
        unique_together = ['agno_radicado', 'cod_tipo_radicado']

class MediosSolicitud(models.Model):
    id_medio_solicitud = models.SmallAutoField(primary_key=True, db_column='T253IdMedioSolicitud')
    nombre = models.CharField(max_length=50, db_column='T253nombre',unique=True)
    aplica_para_pqrsdf = models.BooleanField(default=False, db_column='T253aplicaParaPQRSDF')
    aplica_para_tramites = models.BooleanField(default=False, db_column='T253aplicaParaTramites')
    aplica_para_otros = models.BooleanField(default=False, db_column='T253aplicaParaOtros')
    registro_precargado = models.BooleanField(default=False, db_column='T253registroPrecargado')
    activo = models.BooleanField(default=False, db_column='T253activo')
    item_ya_usado = models.BooleanField(default=False, db_column='T253itemYaUsado')

    class Meta:
        db_table = 'T253MediosSolicitud'  
        verbose_name = 'Medio de Solicitud'  
        verbose_name_plural = 'Medios de Solictud' 


class EstadosSolicitudes(models.Model):
    id_estado_solicitud = models.SmallAutoField(primary_key=True, db_column='T254IdEstadoSolicitud')
    nombre = models.CharField(max_length=50, db_column='T254nombre')
    aplica_para_pqrsdf = models.BooleanField(db_column='T254aplicaParaPQRSDF')
    aplica_para_tramites = models.BooleanField(db_column='T254aplicaParaTramites')
    aplica_para_otros = models.BooleanField(db_column='T254aplicaParaOtros')
    ubicacion_corporacion = models.CharField(max_length=50, db_column='T254ubiEnCorp',null=True)

    class Meta:
       
        db_table = 'T254EstadosSolicitudes'
        verbose_name = 'Estado de Solicitud'  
        verbose_name_plural = 'Estados de Solictud' 


class T262Radicados(models.Model):
    id_radicado = models.AutoField(primary_key=True, db_column='T262IdRadicado')
    id_modulo_que_radica = models.ForeignKey('modulos_radican',on_delete=models.CASCADE,db_column='T262Id_ModuloQueRadica')
    cod_tipo_radicado = models.CharField(max_length=1, choices=TIPOS_RADICADO_CHOICES, db_column='T262codTipoRadicado')
    prefijo_radicado = models.CharField(max_length=10, db_column='T262prefijoRadicado')
    agno_radicado = models.SmallIntegerField(db_column='T262agnoRadicado')
    nro_radicado = models.CharField(max_length=20, db_column='T262nroRadicado')
    fecha_radicado = models.DateTimeField(db_column='T262fechaRadicado')
    id_persona_radica = models.ForeignKey('geojson.Personas',on_delete=models.CASCADE,db_column='T262Id_PersonaRadica')
    id_radicado_asociado = models.ForeignKey('self',on_delete=models.CASCADE,null=True, db_column='T262Id_RadicadoAsociado')

    class Meta:
        unique_together = [
            ("cod_tipo_radicado", "prefijo_radicado", "agno_radicado", "nro_radicado")
        ]
        db_table = 'T262Radicados'  # Nombre de la tabla personalizado

class modulos_radican(models.Model):
    id_ModuloQueRadica = models.AutoField(primary_key=True,db_column='T261Id_ModuloQueRadica')
    nombre = models.CharField(max_length=100,unique=True,db_column='T261nombre')

    class Meta:
        db_table = 'T261ModulosQueRadican'

class PQRSDF(models.Model):
    id_PQRSDF = models.AutoField(primary_key=True, db_column='T257IdPQRSDF')
    cod_tipo_PQRSDF = models.CharField(max_length=2,choices=TIPOS_PQR,db_column='T257codTipoPQRSDF')#,max_length=2,choices=TIPOS_PQR
    id_persona_titular = models.ForeignKey('geojson.Personas',null=True,on_delete=models.CASCADE,db_column='T257Id_PersonaTitular', related_name='persona_titular_relacion')# models.ForeignKey('geojson.Personas',null=True, on_delete=models.CASCADE,
    id_persona_interpone = models.ForeignKey('geojson.Personas',null=True,on_delete=models.CASCADE,db_column='T257Id_PersonaInterpone',related_name='persona_interpone_relacion')
    cod_relacion_con_el_titular = models.CharField(max_length=2, null=True, choices=RELACION_TITULAR, db_column='T257codRelacionConElTitular')
    es_anonima = models.BooleanField(default=False, db_column='T257esAnonima')
    fecha_registro = models.DateTimeField(db_column='T257fechaRegistro')
    id_medio_solicitud = models.ForeignKey(MediosSolicitud,on_delete=models.CASCADE,db_column='T257Id_MedioSolicitud')
    cod_forma_presentacion = models.CharField(max_length=1, choices=FORMA_PRESENTACION, db_column='T257codFormaPresentacion')
    asunto = models.CharField(max_length=100, db_column='T257asunto')
    descripcion = models.CharField(max_length=500, db_column='T257descripcion')
    cantidad_anexos = models.SmallIntegerField(db_column='T257cantidadAnexos')
    nro_folios_totales = models.SmallIntegerField(db_column='T257nroFoliosTotales')
    requiere_rta = models.BooleanField(default=False, db_column='T257requiereRta')
    dias_para_respuesta = models.SmallIntegerField(db_column='T257diasParaRespuesta', null=True)
    id_sucursal_especifica_implicada = models.ForeignKey(SucursalesEmpresas,on_delete=models.CASCADE,db_column='T257Id_SucursalEspecificaImplicada', null=True)
    id_persona_recibe = models.ForeignKey('geojson.Personas',on_delete=models.CASCADE,db_column='T257Id_PersonaRecibe', null=True,related_name='persona_recibe_ralacion')
    id_sucursal_recepcion_fisica = models.ForeignKey(SucursalesEmpresas,on_delete=models.CASCADE,db_column='T257Id_Sucursal_RecepcionFisica', null=True,related_name='sucursal_recepciona_ralacion')
    id_radicado = models.ForeignKey(T262Radicados,on_delete=models.CASCADE,db_column='T257Id_Radicado', null=True)
    fecha_radicado = models.DateTimeField(db_column='T257fechaRadicado', null=True)
    requiere_digitalizacion = models.BooleanField(default=False, db_column='T257requiereDigitalizacion')
    fecha_envio_definitivo_a_digitalizacion = models.DateTimeField(db_column='T257fechaEnvioDefinitivoADigitalizacion', null=True)
    fecha_digitalizacion_completada = models.DateTimeField(db_column='T257fechaDigitalizacionCompletada', null=True)
    fecha_rta_final_gestion = models.DateTimeField(db_column='T257fechaRtaFinalGestion', null=True)
    id_persona_rta_final_gestion = models.ForeignKey('geojson.Personas',on_delete=models.CASCADE,db_column='T257Id_PersonaRtaFinalGestion', null=True,related_name='persona_rta_final_gestion_ralacion')
    id_estado_actual_solicitud = models.ForeignKey(EstadosSolicitudes,on_delete=models.CASCADE,db_column='T257Id_EstadoActualSolicitud')
    fecha_ini_estado_actual = models.DateTimeField(db_column='T257fechaIniEstadoActual')
    id_doc_dearch_exp = models.ForeignKey(DocumentosDeArchivoExpediente,on_delete=models.SET_NULL, blank=True, null=True, db_column='T257Id_DocDeArch_Exp')
    id_expediente_doc = models.ForeignKey(ExpedientesDocumentales,on_delete=models.SET_NULL, blank=True, null=True, db_column='T257Id_ExpedienteDoc')

    class Meta:
       
        db_table = 'T257PQRSDF'

class Otros(models.Model):
    id_otros = models.AutoField(primary_key=True, db_column='T301IdOtros')
    id_persona_titular = models.ForeignKey('geojson.Personas', on_delete=models.CASCADE, related_name='id_persona_titular_otros', db_column='T301Id_PersonaTitular')
    id_persona_interpone = models.ForeignKey('geojson.Personas', on_delete=models.CASCADE, related_name='id_persona_interpone_otros', db_column='T301Id_PersonaInterpone')
    cod_relacion_titular = models.CharField(max_length=2,null=True,blank=True, choices=cod_relacion_persona_titular_CHOICES, db_column='T301codRelacionConElTitular')
    fecha_registro = models.DateTimeField(db_column='T301fechaRegistro')
    id_medio_solicitud = models.ForeignKey (MediosSolicitud, on_delete=models.CASCADE, db_column='T301Id_MedioSolicitud')
    cod_forma_presentacion = models.CharField(max_length=1, choices=cod_forma_presentacion_CHOICES, db_column='T301codFormaPresentacion')
    asunto = models.CharField(max_length=100, db_column='T301asunto')
    descripcion = models.CharField(max_length=150, db_column='T301descripcion')
    cantidad_anexos = models.SmallIntegerField(db_column='T301cantidadAnexos')
    nro_folios_totales = models.SmallIntegerField(db_column='T301nroFoliosTotales')
    id_persona_recibe = models.ForeignKey('geojson.Personas', on_delete=models.SET_NULL, related_name='id_persona_recibe_otros', blank=True, null=True, db_column='T301Id_PersonaRecibe')
    id_sucursal_recepciona_fisica = models.ForeignKey(SucursalesEmpresas, on_delete=models.SET_NULL, blank=True, null=True, db_column='T301Id_Sucursal_RecepcionFisica')
    id_radicados = models.ForeignKey(T262Radicados, on_delete=models.SET_NULL, blank=True, null=True, db_column='T301Id_Radicado')
    fecha_radicado = models.DateTimeField(blank=True, null=True,db_column='T301fechaRadicado')
    requiere_digitalizacion = models.BooleanField(db_column='T301requiereDigitalizacion')
    fecha_envio_definitivo_digitalizacion = models.DateTimeField(blank=True, null=True,db_column='T301fechaEnvioDefinitivoADigitalizacion')
    fecha_digitalizacion_completada = models.DateTimeField(blank=True, null=True,db_column='T301fechaDigitalizacionCompletada')
    id_estado_actual_solicitud = models.ForeignKey (EstadosSolicitudes, on_delete=models.CASCADE, db_column='T301Id_EstadoActualSolicitud')
    fecha_inicial_estado_actual = models.DateTimeField(db_column='T301fechaIniEstadoActual')
    id_documento_archivo_expediente = models.ForeignKey(DocumentosDeArchivoExpediente, on_delete=models.SET_NULL, blank=True, null=True, db_column='T301Id_DocDeArch_Exp')
    id_expediente_documental = models.ForeignKey(ExpedientesDocumentales, on_delete=models.SET_NULL, blank=True, null=True, db_column='T301Id_ExpedienteDoc')

    class Meta:
        db_table = 'T301Otros'
        verbose_name = 'Otro'
        verbose_name_plural = 'Otros'
    
class Estados_PQR(models.Model):
    id_estado_PQR = models.AutoField(primary_key=True, db_column='T255IdEstado_PQR_Otros')
    PQRSDF = models.ForeignKey(PQRSDF,on_delete=models.CASCADE,db_column='T255Id_PQRSDF', null=True)
    solicitud_usu_sobre_PQR = models.ForeignKey('SolicitudAlUsuarioSobrePQRSDF',on_delete=models.CASCADE,db_column='T255Id_SolicitudAlUsuSobrePQR', null=True)#PENDIENTE MODELO T266
    id_otros = models.ForeignKey(Otros,on_delete=models.SET_NULL, blank=True, null=True,db_column='T255Id_Otros')
    id_tramite = models.ForeignKey('geojson.SolicitudesTramites', models.SET_NULL, db_column='T255Id_SolicitudTramite', blank=True, null=True)
    estado_solicitud = models.ForeignKey(EstadosSolicitudes,on_delete=models.CASCADE,db_column='T255Id_EstadoSolicitud')
    fecha_iniEstado = models.DateTimeField(db_column='T255fechaIniEstado')
    persona_genera_estado = models.ForeignKey('geojson.Personas',on_delete=models.CASCADE,db_column='T255Id_PersonaGeneraEstado', null=True)
    estado_PQR_asociado = models.ForeignKey('self',on_delete=models.CASCADE,db_column='T255Id_Estado_PQR_Asociado', null=True)#PENDIENTE MODELO T255

    class Meta:
       # managed = False  # Evita que Django gestione esta tabla en la base de datos.
        db_table = 'T255Estados_PQR_Otros'

class SolicitudAlUsuarioSobrePQRSDF(models.Model):
    id_solicitud_al_usuario_sobre_pqrsdf = models.AutoField(primary_key=True, db_column='T266IdSolicitudAlUsuarioSobrePQR')
    id_pqrsdf = models.ForeignKey(PQRSDF, on_delete =models.SET_NULL, db_column='T266Id_PQRSDF',null=True,blank=True)
    id_solicitud_tramite = models.ForeignKey('geojson.SolicitudesTramites',on_delete= models.SET_NULL, db_column='T266Id_SolicitudTramite',null=True,blank=True)
    id_persona_solicita = models.ForeignKey('geojson.Personas', models.CASCADE, db_column='T266Id_PersonaSolicita')
    id_und_org_oficina_solicita = models.ForeignKey(UnidadesOrganizacionales, models.CASCADE, db_column='T266Id_UndOrgOficina_Solicita')
    cod_tipo_oficio = models.CharField(max_length=1,choices=TIPOS_OFICIO_CHOICES,db_column='T266codTipoOficio')
    fecha_solicitud = models.DateTimeField(db_column='T66fechaSolicitud')
    asunto = models.CharField(max_length=100, db_column='T266asunto')
    descripcion = models.CharField(max_length=500, db_column='T266descripcion')
    cantidad_anexos = models.SmallIntegerField(null=True, db_column='T266cantidadAnexos')
    nro_folios_totales = models.SmallIntegerField(null=True, db_column='T266nroFoliosTotales')
    dias_para_respuesta = models.SmallIntegerField(null=True, db_column='T266diasParaRespuesta')
    id_radicado_salida = models.ForeignKey(T262Radicados, models.SET_NULL, db_column='T266Id_RadicadoSalida', blank=True, null=True)
    fecha_radicado_salida = models.DateTimeField(db_column='T266fechaRadicadoSalida', blank=True, null=True)
    id_estado_actual_solicitud = models.ForeignKey(EstadosSolicitudes, models.CASCADE, db_column='T266Id_EstadoActualSolicitud')
    fecha_ini_estado_actual = models.DateTimeField(db_column='T266fechaIniEstadoActual')
    id_doc_de_archivo_exp = models.ForeignKey(DocumentosDeArchivoExpediente, models.SET_NULL, db_column='T266Id_DocDeArch_Exp', blank=True, null=True)
    
    class Meta:
        db_table = 'T266SolicitudAlUsuarioSobrePQRSDF'


class Anexos(models.Model):
    id_anexo = models.AutoField(primary_key=True, db_column='T258IdAnexo')
    nombre_anexo = models.CharField(max_length=50, db_column='T258nombreAnexo')
    orden_anexo_doc = models.SmallIntegerField(db_column='T258ordenAnexoEnElDoc')
    cod_medio_almacenamiento = models.CharField(max_length=2, choices=medio_almacenamiento_CHOICES, db_column='T258codMedioAlmacenamiento')
    medio_almacenamiento_otros_Cual = models.CharField(max_length=30, db_column='T258medioAlmacenamientoOtros_Cual', null=True)
    numero_folios = models.SmallIntegerField(db_column='T258numeroFolios')
    ya_digitalizado = models.BooleanField(db_column='T258yaDigitalizado')
    observacion_digitalizacion = models.CharField(max_length=100, db_column='T258observacionDigitalizacion', null=True)
    id_docu_arch_exp = models.ForeignKey(DocumentosDeArchivoExpediente, blank=True, null=True, on_delete=models.SET_NULL, db_column='T258Id_DocuDeArch_Exp')

    class Meta:
        #managed = False  # Evita que Django gestione esta tabla en la base de datos.
        db_table = 'T258Anexos'


class MetadatosAnexosTmp(models.Model):
    id_metadatos_anexo_tmp = models.AutoField(primary_key=True, db_column='T260IdMetadatos_Anexo_Tmp')
    id_anexo = models.ForeignKey(Anexos, on_delete=models.CASCADE, db_column='T260Id_Anexo')
    nombre_original_archivo = models.CharField(max_length=50, db_column='T260nombreOriginalDelArchivo', null=True)
    fecha_creacion_doc = models.DateTimeField(db_column='T260fechaCreacionDoc', null=True)
    descripcion = models.CharField(max_length=500, db_column='T260descripcion', null=True)
    asunto = models.CharField(max_length=150, db_column='T260asunto', null=True)
    cod_categoria_archivo = models.CharField(max_length=2, choices=tipo_archivo_CHOICES, db_column='T260codCategoriaArchivo', null=True)
    es_version_original = models.BooleanField(db_column='T260esVersionOriginal',null=True)
    tiene_replica_fisica = models.BooleanField(db_column='T260tieneReplicaFisica',null=True)
    nro_folios_documento = models.SmallIntegerField(db_column='T260nroFoliosDocumento',null=True)
    cod_origen_archivo = models.CharField(max_length=1, choices=origen_archivo_CHOICES, db_column='T260codOrigenArchivo',null=True)
    id_tipologia_doc = models.ForeignKey(TipologiasDoc, on_delete=models.SET_NULL, blank=True, null=True, db_column='T260Id_TipologiaDoc')
    cod_tipologia_doc_Prefijo = models.CharField(max_length=10, db_column='T260codTipologiaDoc_Prefijo', null=True)
    cod_tipologia_doc_agno = models.SmallIntegerField(db_column='T260codTipologiaDoc_Agno', null=True)
    cod_tipologia_doc_Consecutivo = models.CharField(max_length=20, db_column='T260codTipologiaDoc_Consecutivo', null=True)
    tipologia_no_creada_TRD = models.CharField(max_length=50, db_column='T260tipologiaNoCreadaEnTRD', null=True)
    palabras_clave_doc = models.CharField(max_length=255, db_column='T260palabrasClaveDoc', null=True)
    id_archivo_sistema = models.ForeignKey(ArchivosDigitales, on_delete=models.CASCADE, db_column='T260Id_ArchivoEnSistema')

    class Meta:
        #managed = False  # Evita que Django gestione esta tabla en la base de datos.
        db_table = 'T260Metadatos_Anexos_Tmp'
        unique_together = ('id_anexo',)  # Restricción para que Id_Anexo sea único


class AsignacionTramites(models.Model):
    id_asignacion_tramite = models.AutoField(db_column='T279IdAsignacion_Tramite', primary_key=True)
    id_solicitud_tramite = models.ForeignKey('geojson.SolicitudesTramites',on_delete=models.CASCADE,db_column='T279Id_SolicitudTramite')
    consecutivo_asign_x_tramite = models.SmallIntegerField(db_column='T279consecutivoAsignXTramite', null=True, blank=True)
    fecha_asignacion = models.DateTimeField(db_column='T279fechaAsignacion', null=True, blank=True)
    id_persona_asigna = models.ForeignKey('geojson.Personas',on_delete = models.CASCADE,db_column='T279Id_PersonaAsigna',related_name='persona_asigna_tramite')
    id_persona_asignada =  models.ForeignKey('geojson.Personas',on_delete = models.CASCADE,db_column='T279Id_PersonaAsignada',related_name='persona_asignada_tramites')
    cod_estado_asignacion = models.CharField(max_length=2,
                                             choices=[('Ac', 'Aceptado'),('Re', 'Rechazado')], db_column='T279codEstadoAsignacion',null=True,blank=True)
    fecha_eleccion_estado = models.DateTimeField(db_column='T279fechaEleccionEstado',null=True,blank=True)
    justificacion_rechazo = models.CharField(db_column='T279justificacionRechazo', max_length=250, null=True, blank=True)
    asignacion_de_ventanilla = models.BooleanField(db_column='T279asignacionDeVentanilla')
    id_und_org_seccion_asignada = models.ForeignKey(UnidadesOrganizacionales,on_delete=models.SET_NULL,null=True,blank=True,db_column='T279Id_UndOrgSeccion_Asignada',related_name='unidad_asignada_tramites')
    id_und_org_oficina_asignada = models.ForeignKey(UnidadesOrganizacionales,on_delete=models.SET_NULL,null=True,blank=True,db_column='T279Id_UndOrgOficina_Asignada')
    id_catalogo_serie_subserie = models.IntegerField(db_column='T279id_CatSeries_UndOrg_CCD', null=True, blank=True)
    class Meta:
        db_table = 'T279Asignacion_Tramites'
        unique_together = (('id_solicitud_tramite', 'consecutivo_asign_x_tramite'),)
