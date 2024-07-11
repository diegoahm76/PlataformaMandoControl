from django.db import models
from geojson.models.base_models import Municipio, Paises

class SucursalesEmpresas(models.Model):
    id_sucursal_empresa = models.AutoField(primary_key=True, editable=False, db_column='T012IdSucursalEmpresa')
    id_persona_empresa = models.ForeignKey('geojson.Personas',on_delete=models.CASCADE, db_column='T012Id_PersonaEmpresa')
    numero_sucursal = models.SmallIntegerField(db_column='T012nroSucursal')
    descripcion_sucursal = models.CharField(max_length=255, db_column='T012descripcionSucursal')
    direccion = models.CharField(max_length=255, db_column='T012dirSucursal')
    direccion_sucursal_georeferenciada_lat = models.DecimalField(max_digits=18, decimal_places=13, null=True, blank=True, db_column='T012dirSucursalGeorefLat')
    direccion_sucursal_georeferenciada_lon = models.DecimalField(max_digits=18, decimal_places=13, null=True, blank=True, db_column='T012dirSucursalGeorefLon')
    municipio = models.ForeignKey(Municipio, related_name='municipio_sucursales', on_delete=models.SET_NULL, null=True, blank=True, db_column='T012Cod_MunicipioSucursalNal')
    pais_sucursal_exterior = models.ForeignKey(Paises, on_delete=models.SET_NULL, null=True, blank=True, db_column='T012Cod_PaisSucursalExterior')
    direccion_notificacion = models.CharField(max_length=255, null=True, blank=True, db_column='T012dirNotificacionNal')
    direccion_notificacion_referencia = models.CharField(max_length=255, null=True, blank=True, db_column='T012dirNotificacionNalReferencia')
    municipio_notificacion = models.ForeignKey(Municipio, related_name='municipio_notificacion_sucursales', on_delete=models.SET_NULL, null=True, blank=True, db_column='T012Cod_MunicipioNotificacionNal') 
    email_sucursal = models.EmailField(max_length=100, null=True, blank=True, db_column='T012emailSucursal')
    telefono_sucursal = models.CharField(max_length=15, null=True, blank=True, db_column='T012telContactoSucursal')
    es_principal = models.BooleanField(default=True, db_column='T012esPrincipal')
    activo = models.BooleanField(default=True, db_column='T012activo')
    item_ya_usado = models.BooleanField(default=False, db_column='T012itemYaUsado')
    
    def __str__(self):
        return str(self.descripcion_sucursal)
    
    class Meta:
        db_table = 'T012SucursalesEmpresa'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        unique_together = [('id_persona_empresa','descripcion_sucursal'), ('numero_sucursal','id_persona_empresa')]
