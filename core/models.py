from django.db import models
from django.contrib.auth.models import User

class SecurityIncident(models.Model):
    title = models.CharField(max_length=255)  # Text curt
    description = models.TextField()          # Text llarg
    severity = models.CharField(max_length=50)  # Alta / Mitjana / Baixa
    detected_at = models.DateTimeField()      # Data i hora

    def __str__(self):
        return self.title

class Incident(models.Model):
    titol = models.CharField(max_length=100)
    descripcio = models.TextField()
    propietari = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titol