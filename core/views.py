from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Importem el model d'usuaris de Django
from .models import Incident

@login_required
def perfil_usuari(request):
    # Simplement renderitza la pàgina de perfil
    return render(request, 'perfil.html')

@login_required
def cerca_incidents(request):
    query = request.GET.get('q', '')
    
    # --- HARDENING: Substituïm el SQL manual per l'ORM ---
    if query:
        # L'ORM genera automàticament una consulta parametritzada i segura.
        # '__icontains' equival a un LIKE '%query%' però protegit.
        incidents = User.objects.filter(username__icontains=query)
    else:
        incidents = []
    
    return render(request, 'cerca.html', {'incidents': incidents, 'query': query})

@login_required
def actualitzar_correu(request):
    missatge = ""
    if request.method == 'POST':
        nou_email = request.POST.get('email', '')
        
        # --- HARDENING: Substituïm cursor.execute() per mètodes de l'ORM ---
        # Obtenim l'objecte usuari i actualitzem el camp email.
        # Django s'encarrega de netejar les dades abans d'enviar-les a la DB.
        usuari = User.objects.get(id=request.user.id)
        usuari.email = nou_email
        usuari.save()
        
        missatge = "Correu actualitzat correctament amb seguretat ORM!"
        
    return render(request, 'actualitzar_correu.html', {'missatge': missatge})

@login_required
# Canvia 'id' per 'incident_id' per coincidir amb la teva URL
def detall_incident(request, incident_id):  
    # I aquí també l'has de fer servir:
    incident = get_object_or_404(Incident, id=incident_id, propietari=request.user)
    
    return render(request, 'detall_incident.html', {'incident': incident})