from django.db import models

class Paises(models.Model):
    cod_pais = models.CharField(primary_key=True, max_length=2, db_column='T003CodPais')
    nombre = models.CharField(max_length=50, unique=True, db_column='T003nombre')
    
    def __str__(self):
        return str(self.cod_pais)
    
    class Meta:
        db_table = "T003Paises"
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'

class Municipio(models.Model):
    cod_municipio = models.CharField(primary_key=True, max_length=5, db_column='T001CodMunicipio')
    nombre = models.CharField(max_length=30, db_column='T001nombre')
    cod_departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE, db_column='T001Cod_Departamento')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T001MunicipiosDepartamento'
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        unique_together = (('nombre', 'cod_departamento'),)
        
class Departamento(models.Model):
    cod_departamento = models.CharField(primary_key=True, max_length=2, db_column='T002CodDepartamento')
    nombre = models.CharField(max_length=50, unique=True, db_column='T002nombre')
    pais = models.ForeignKey(Paises, on_delete=models.CASCADE, db_column='T002Cod_Pais')

    def __str__(self):
        return str(self.nombre)

    class Meta:
        db_table = 'T002DepartamentosPais'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

class Sexo(models.Model):
    cod_sexo = models.CharField(primary_key=True, max_length=1, db_column='T004CodSexo')
    nombre = models.CharField(max_length=20, unique=True, db_column='T004nombre')

    def __str__(self):  
        return str(self.nombre)
    
    class Meta:
        db_table = 'T004Sexo'
        verbose_name = 'Sexo'
        verbose_name_plural = 'Sexo'
        
class EstadoCivil(models.Model):
    cod_estado_civil = models.CharField(max_length=1, primary_key=True, db_column='T005CodEstadoCivil')
    nombre = models.CharField(max_length=20, unique=True, db_column='T005nombre')
    precargado = models.BooleanField(default=False, db_column='T005registroPrecargado')
    activo = models.BooleanField(default=True, db_column='T005activo')
    item_ya_usado = models.BooleanField(default=False, db_column='T005itemYaUsado')
    
    def __str__(self):
        return str(self.nombre)
    
    class Meta:
        db_table = 'T005EstadoCivil'
        verbose_name = 'Estado civil'
        verbose_name_plural = 'Estados civiles'

class TipoDocumento(models.Model):
    cod_tipo_documento = models.CharField(max_length=2, primary_key=True, db_column='T006CodTipoDocumentoID')
    nombre = models.CharField(max_length=40, unique=True, db_column='T006nombre')
    precargado = models.BooleanField(default=False, db_column='T006registroPrecargado')
    activo = models.BooleanField(default=True, db_column='T006activo')
    item_ya_usado = models.BooleanField(default=False, db_column='T006itemYaUsado')
    def __str__(self):
        return str(self.nombre)
    
    class Meta:
        db_table = 'T006TiposDocumentoID'
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documentos'
        

class Cargos(models.Model):
    id_cargo = models.SmallAutoField(primary_key=True, editable=False, db_column='T009IdCargo')
    nombre = models.CharField(max_length=50, unique=True, db_column='T009nombre')
    activo = models.BooleanField(default=True, db_column='T009activo')
    item_usado = models.BooleanField(default=False, db_column='T009itemYaUsado')
    
    def __str__(self):
        return str(self.nombre)
        
    class Meta:
        db_table = 'T009Cargos'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

class TipoRenta(models.Model):
    id_tipo_renta = models.AutoField(primary_key=True, db_column='T442IdTipoRenta')
    cod_tipo_renta = models.CharField(max_length=5, blank=True, null=True, db_column='T442codTipoRenta')
    nombre_tipo_renta = models.CharField(max_length=100, blank=True, null=True, db_column='T442Nombre')
    descripcion = models.CharField(max_length=255, blank=True, null=True, db_column='T442Descripcion')
    precargado = models.BooleanField(default=False, db_column='T442Precargado')

    # valor_tipo_renta = models.DecimalField(max_digits=10, decimal_places=2, db_column='T442valor_tipo_renta')
    class Meta:
        db_table = 'T442TipoRenta'
        verbose_name = 'Tipo Renta'
        verbose_name_plural = 'Tipos de Renta'