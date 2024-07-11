from django.db import models

class T920Expediente(models.Model):
    t920codcia = models.CharField(max_length=5, db_column='t920codcia', null=True)
    t920codexpediente = models.CharField(max_length=30, db_column='t920codexpediente', null=True)
    t920codtipoexpcorp = models.CharField(max_length=5, db_column='t920codtipoexpcorp', null=True)
    t920numexpedientesila = models.CharField(max_length=30, db_column='t920numexpedientesila', null=True)
    t920codexpedienterel = models.CharField(max_length=30, db_column='t920codexpedienterel', null=True)
    t920descripcion = models.CharField(max_length=255, db_column='t920descripcion', null=True)
    t920codestadoexp = models.CharField(max_length=5, db_column='t920codestadoexp', null=True)
    t920idtramiteppal = models.CharField(max_length=30, db_column='t920idtramiteppal', null=True)

    class Meta:
        db_table = 'rt920expediente'



class Tercero(models.Model):
    t03codcia = models.CharField(max_length=5, db_column='t03codcia', null=True)
    t03nit = models.CharField(max_length=15, db_column='t03nit', null=True)
    t03codciudadced = models.CharField(max_length=5, db_column='t03codciudadced', null=True)
    t03codrapido = models.CharField(max_length=5, db_column='t03codrapido', null=True)
    t03libretamil = models.CharField(max_length=20, db_column='t03libretamil', null=True)
    t03matriprof = models.CharField(max_length=30, db_column='t03matriprof', null=True)
    t03nombre = models.CharField(max_length=255, db_column='t03nombre', null=True)
    t03primerapellido = models.CharField(max_length=255, db_column='t03primerapellido', null=True)
    t03segundoapellido = models.CharField(max_length=255, db_column='t03segundoapellido', null=True)
    t03primernombre = models.CharField(max_length=255, db_column='t03primernombre', null=True)
    t03segundonombre = models.CharField(max_length=255, db_column='t03segundonombre', null=True)
    t03codpostal = models.CharField(max_length=20, db_column='t03codpostal', null=True)
    t03direccion = models.CharField(max_length=100, db_column='t03direccion', null=True)
    t03telefono = models.CharField(max_length=100, db_column='t03telefono', null=True)
    t03fax = models.CharField(max_length=100, db_column='t03fax', null=True)
    t03email = models.CharField(max_length=100, db_column='t03email', null=True)
    t03website = models.CharField(max_length=100, db_column='t03website', null=True)
    t03codtiposociedad = models.CharField(max_length=5, db_column='t03codtiposociedad', null=True)
    t03fechaingreso = models.DateTimeField(db_column='t03fechaingreso', null=True)
    t03codcalifica = models.CharField(max_length=5, db_column='t03codcalifica', null=True)
    t03observacion = models.TextField(db_column='t03observacion', null=True)
    t03cargoexterno = models.CharField(max_length=100, db_column='t03cargoexterno', null=True)
    t03nitrel = models.CharField(max_length=15, db_column='t03nitrel', null=True)
    t03codtiporegimen = models.CharField(max_length=5, db_column='t03codtiporegimen', null=True)
    t03tiposeparanombre = models.SmallIntegerField(db_column='t03tiposeparanombre', null=True)
    t03coddpto = models.CharField(max_length=5, db_column='t03coddpto', null=True)
    t03codmpio = models.CharField(max_length=5, db_column='t03codmpio', null=True)
    t03codcgn = models.CharField(max_length=10, db_column='t03codcgn', null=True)
    t03codctacontabcausa = models.CharField(max_length=20, db_column='t03codctacontabcausa', null=True)
    t03codactrut1 = models.CharField(max_length=10, db_column='t03codactrut1', null=True)
    t03codactrut = models.CharField(max_length=10, db_column='t03codactrut', null=True)
    t03codactrut3 = models.CharField(max_length=10, db_column='t03codactrut3', null=True)
    t03codpais = models.CharField(max_length=4, db_column='t03codpais', null=True)
    t03codtipodocumid = models.CharField(max_length=5, db_column='t03codtipodocumid', null=True)
    t03codreciproca = models.CharField(max_length=15, db_column='t03codreciproca', null=True)
    t03entaseguradora = models.CharField(max_length=100, db_column='t03entaseguradora', null=True)
    t03codentchip = models.CharField(max_length=9, db_column='t03codentchip', null=True)
    t03fechanacimiento = models.DateTimeField(db_column='t03fechanacimiento', null=True)
    t03genero = models.CharField(max_length=20, db_column='t03genero', null=True)
    t03actcertifpyg = models.CharField(max_length=1, db_column='t03actcertifpyg', null=True)
    t03fechaactwebinfo = models.DateTimeField(db_column='t03fechaactwebinfo', null=True)
    t03fechasolwebinfo = models.DateTimeField(db_column='t03fechasolwebinfo', null=True)
    t03ipaddractserv = models.CharField(max_length=50, db_column='t03ipaddractserv', null=True)
    t03webpassword = models.CharField(max_length=10, db_column='t03webpassword', null=True)
    t03actrecibosicar = models.CharField(max_length=1, db_column='t03actrecibosicar', null=True)
    t03id_pci_siif = models.CharField(max_length=50, db_column='t03id_pci_siif', null=True)

    class Meta:
        db_table = 'rt03tercero'