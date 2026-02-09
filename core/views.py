from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection  # Necessari per usar el cursor directament

@login_required
def perfil_usuari(request):
    return render(request, 'perfil.html')

@login_required
def cerca_incidents(request):
    query = request.GET.get('q', '')
    incidents = []

    if query:
        cursor = connection.cursor()
        
        sql = "SELECT id, username, email FROM auth_user WHERE username LIKE '%" + query + "%'"
        
        cursor.execute(sql)
        incidents = cursor.fetchall()
    
    return render(request, 'cerca.html', {'incidents': incidents, 'query': query})

@login_required
def actualitzar_correu(request):
    missatge = ""
    if request.method == 'POST':
        nou_email = request.POST.get('email', '')
        user_id = request.user.id
        
        cursor = connection.cursor()
        # LÍNIA CRÍTICA: Vulnerable a SQL Injection
        sql = f"UPDATE auth_user SET email = '{nou_email}' WHERE id = {user_id}"
        
        cursor.execute(sql)
        missatge = "Correu actualitzat correctament!"
        
    return render(request, 'actualitzar_correu.html', {'missatge': missatge})