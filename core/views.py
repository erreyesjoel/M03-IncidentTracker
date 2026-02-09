from django.shortcuts import render
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
def detall_incident(request, incident_id):
    # VULNERABILITAT: Només filtrem per ID, no per propietari!
    incident = Incident.objects.get(id=incident_id)
    return render(request, 'detall_incident.html', {'incident': incident})