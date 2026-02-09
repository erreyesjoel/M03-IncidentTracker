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