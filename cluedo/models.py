from django.db import models

# Create your models here.
class GameState(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    assassin = models.CharField(max_length=10, null=True, blank=True)
    case_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Juego: caso {self.case_id}, asesino {self.assassin}"