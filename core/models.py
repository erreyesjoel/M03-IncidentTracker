from django.db import models

class SecurityIncident(models.Model):
    title = models.CharField(max_length=255)  # Text curt
    description = models.TextField()          # Text llarg
    severity = models.CharField(max_length=50)  # Alta / Mitjana / Baixa
    detected_at = models.DateTimeField()      # Data i hora

    def __str__(self):
        return self.title
