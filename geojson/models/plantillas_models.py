from django.db import models

from geojson.choices.tipo_acceso_choices import tipo_acceso_CHOICES

class PlantillasDoc(models.Model):
    id_plantilla_doc = models.AutoField(primary_key=True, db_column='T200IdPlantillaDoc')
    nombre = models.CharField(max_length=100,unique=True, db_column='T200nombre')
    descripcion = models.CharField(max_length=255, db_column='T200descripcion', null=True, blank=True)
    id_archivo_digital = models.ForeignKey('geojson.ArchivosDigitales',on_delete=models.CASCADE,db_column='T200Id_ArchivoDigital')
    id_formato_tipo_medio = models.ForeignKey('geojson.FormatosTiposMedio',on_delete=models.CASCADE,db_column='T200Id_Formato_TipoMedio')
    asociada_a_tipologia_doc_trd = models.BooleanField(db_column='T200asociadaATipologiaDocTRD')
    id_tipologia_doc_trd = models.ForeignKey('geojson.TipologiasDoc',on_delete=models.CASCADE,db_column='T200Id_TipologiaDocTRD', null=True, blank=True)
    otras_tipologias = models.CharField(max_length=30, db_column='T200otrasTipologias', null=True, blank=True)
    codigo_formato_calidad_asociado = models.CharField(max_length=30, db_column='T200codigoFormatoCalidadAsociado')
    version_formato_calidad_asociado = models.DecimalField(max_digits=5, decimal_places=2, db_column='T200versionFormatoCalidadAsociado')
    cod_tipo_acceso = models.CharField(max_length=2,choices=tipo_acceso_CHOICES, db_column='T200codTipoAcceso')
    observacion = models.CharField(max_length=255, db_column='T200observacion', null=True, blank=True)
    activa = models.BooleanField(default=True, db_column='T200activa')
    fecha_creacion = models.DateTimeField(auto_now=True, db_column='T200fechaCreacion')
    id_persona_crea_plantilla = models.ForeignKey('geojson.Personas', on_delete=models.CASCADE, db_column='T200Id_PersonaCreaPlantilla')
    class Meta:
        db_table = 'T200PlantillasDoc'
        

    def __str__(self):
        return self.nombre