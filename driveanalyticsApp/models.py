from django.db import models

# Create your models here.
class DimVehiculo(models.Model):
    id_vehiculo = models.IntegerField(primary_key=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    year = models.IntegerField()
    tipo = models.CharField(max_length=50)
    cilindraje = models.IntegerField()
    #id_sucursal = models.IntegerField(foreign_key=True)
    estado = models.CharField(max_length=20)
    fecha_registro = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'dim_vehiculo' # nombre de la tabla en la base de datos
        managed = False # Django no gestionará la creación de esta tabla