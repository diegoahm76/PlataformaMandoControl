from django.db import models
from geojson.models.base_models import TipoRenta
from geojson.models.extraccion_model_recaudo import T920Expediente
from geojson.choices.estados_liquidacion_choices import estados_liquidacion_CHOICES


class Deudores(models.Model):
    id = models.AutoField(primary_key=True, db_column='T410IdDeudor')
    id_persona_deudor_pymisis = models.ForeignKey('geojson.Tercero', on_delete=models.SET_NULL, blank=True, null=True, db_column='T410Id_PersonaDeudorPymisis')
    id_persona_deudor = models.ForeignKey('geojson.Personas', on_delete=models.SET_NULL, blank=True, null=True, db_column='T410Id_PersonaDeudor')

    class Meta:
        db_table = 'T410Deudores'
        verbose_name = 'Deudor'
        verbose_name_plural = 'Deudores'


class Expedientes(models.Model):
    id = models.AutoField(primary_key=True, db_column='T407IdExpediente')
    id_deudor = models.ForeignKey(Deudores, on_delete=models.CASCADE, db_column='T407Id_Deudor')
    liquidado = models.BooleanField(default=False, null=True, blank=True, db_column='T407liquidado')
    id_expediente_doc = models.ForeignKey('geojson.ExpedientesDocumentales', on_delete=models.SET_NULL, blank=True, null=True, db_column='T407Id_ExpedienteDoc')
    id_expediente_pimisys = models.ForeignKey(T920Expediente, on_delete=models.SET_NULL, blank=True, null=True, db_column='T407Id_ExpedientePimisys')

    class Meta:
        db_table = 'T407Expedientes'
        verbose_name = 'Expediente'
        verbose_name_plural = 'Expedientes'

class LiquidacionesBase(models.Model):
    id = models.AutoField(primary_key=True, db_column="T403IdLiquidacionBase")
    fecha_liquidacion = models.DateTimeField(db_column="T403fechaLiquidacion")
    vencimiento = models.DateTimeField(db_column="T403vencimiento")
    periodo_liquidacion = models.CharField(max_length=255, db_column="T403periodoLiquidacion")
    valor = models.DecimalField(max_digits=20, decimal_places=4, default=0, db_column="T403Valor")
    estado = models.CharField(choices=estados_liquidacion_CHOICES, max_length=10, db_column="T403estado")
    id_deudor = models.ForeignKey(Deudores, blank=True, null=True, on_delete=models.SET_NULL, db_column="T403Id_Deudor")
    id_expediente = models.ForeignKey(Expedientes, blank=True, null=True, on_delete=models.SET_NULL, db_column="T403Id_Expediente")
    ciclo_liquidacion = models.CharField(max_length=255, blank=True, null=True, db_column="T403cicloliquidacion")
    id_solicitud_tramite = models.ForeignKey('geojson.SolicitudesTramites', blank=True, null=True, on_delete=models.SET_NULL, db_column="T403Id_SolicitudTramite")
    id_archivo = models.ForeignKey('geojson.ArchivosDigitales', blank=True, null=True, on_delete=models.SET_NULL, db_column="T403Id_Archivo")
    id_tipo_renta=models.ForeignKey(TipoRenta, on_delete=models.SET_NULL, db_column='T403Id_TipoRenta',null=True, blank=True)
    num_liquidacion = models.IntegerField(null=True, blank=True, db_column='T403numLiquidacion')
    agno = models.SmallIntegerField(null=True, blank=True, db_column='T403Agno')
    periodo = models.SmallIntegerField(null=True, blank=True, db_column='T403Periodo')
    nit = models.CharField(max_length=15, blank=True, null=True, db_column="T403Nit")
    fecha = models.DateTimeField(null=True, db_column="t403Fecha")
    valor_liq = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, db_column='T403ValorLiq')
    valor_pagado = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, db_column='T403ValorPagado')
    valor_prescripcion = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True, db_column='T403valorPrescripcion')
    anulado = models.CharField(max_length=1, blank=True, null=True, db_column="T403Anulado")
    num_resolucion = models.IntegerField(blank=True, null=True, db_column="T403numResolucion")
    agno_resolucion = models.SmallIntegerField(null=True, blank=True, db_column='T403AgnoResolucion')
    cod_origen_liq = models.CharField(max_length=1, blank=True, null=True, db_column="T403codOrigenLiq")
    observacion = models.CharField(max_length=255, blank=True, null=True, db_column="T403Observacion")
    cod_tipo_beneficio = models.CharField(max_length=5, blank=True, null=True, db_column="T403codTipoBeneficio")
    fecha_contab = models.DateTimeField(null=True, blank=True, db_column="T403fechaContab")
    se_cobra = models.CharField(max_length=1, blank=True, null=True, db_column="T403seCobra")
    fecha_en_firme = models.DateTimeField(null=True, blank=True, db_column="T403fechaEnFirme")
    nnum_origen_liq = models.IntegerField(blank=True, null=True, db_column="T403NnumOrigenLiq")
    id_persona_liquida = models.ForeignKey('geojson.Personas', on_delete=models.SET_NULL, blank=True, null=True, db_column="T403Id_PersonaLiquida")

    class Meta:
        db_table = "T403LiquidacionesBase"
        verbose_name = 'Liquidación base'
        verbose_name_plural = 'Liquidaciones base'