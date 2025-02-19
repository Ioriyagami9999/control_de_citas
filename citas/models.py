from django.db import models
from django.contrib.auth.models import User

class Cita(models.Model):
    fecha_hora = models.DateTimeField()
    paciente = models.CharField(max_length=255, editable=False)
    tipo_cita = models.CharField(max_length=100, choices=[
        ('Consulta', 'Consulta'),
        ('Servicio', 'Servicio'),
        ('Tratamiento', 'Tratamiento')
    ])
    medico = models.CharField(max_length=255)
    numero_cita = models.AutoField(primary_key=True, editable=False)
    eliminado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.paciente} - {self.tipo_cita} ({self.fecha_hora}) - {self.medico} - {self.numero_cita} - {self.eliminado}"
