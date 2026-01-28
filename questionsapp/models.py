from django.db import models

class Question(models.Model):
    number = models.IntegerField(unique=True)
    question = models.TextField()
    options = models.JSONField()
    correct_answer = models.JSONField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pregunta {self.number}"
