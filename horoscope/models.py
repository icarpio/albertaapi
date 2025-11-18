from django.db import models

FECHAS_SIGNOS = {
    "ARIES": "21 de marzo - 20 de abril",
    "TAURO": "21 de abril – 21 de mayo",
    "GÉMINIS": "22 de mayo – 22 de junio",
    "CÁNCER": "23 de junio – 23 de julio",
    "LEO": "24 de julio – 23 de agosto",
    "VIRGO": "24 de agosto - 23 de septiembre",
    "LIBRA": "24 de septiembre - 23 de octubre",
    "ESCORPIO": "24 de octubre - 22 de noviembre",
    "SAGITARIO": "23 de noviembre - 21 de diciembre",
    "CAPRICORNIO": "22 de diciembre - 20 de enero",
    "ACUARIO": "21 de enero - 19 de febrero",
    "PISCIS": "20 de febrero - 20 de marzo"
}

class Horoscopo(models.Model):
    signo = models.CharField(max_length=20)
    fecha = models.DateField(auto_now_add=True)  # fecha de hoy
    rango_fecha = models.CharField(max_length=50, blank=True)
    texto = models.TextField()

    class Meta:
        unique_together = ('signo', 'fecha')
        ordering = ['-fecha']

    def save(self, *args, **kwargs):
        self.rango_fecha = FECHAS_SIGNOS.get(self.signo.upper(), "")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.signo} - {self.fecha}"
