from django.contrib import admin
from .models import SecurityIncident, Incident # Importem els dos

admin.site.register(SecurityIncident)
admin.site.register(Incident) # <--- AQUEST ÉS EL QUE TÉ EL PROPIETARI