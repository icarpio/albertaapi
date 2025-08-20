from django.db import models

class Traduccion(models.Model):
    texto_original = models.TextField()
    español = models.TextField()
    ingles = models.TextField()
    italiano = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto_original[:50]  # muestra los primeros 50 caracteres
