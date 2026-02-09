from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class SQLInjectionTest(TestCase):
    def setUp(self):
        # 1. Creem un usuari normal (no és superuser)
        self.client = Client()
        self.usuari = User.objects.create_user(username='victima', password='password123')
        self.client.login(username='victima', password='password123')

    def test_privilege_escalation_sqli(self):
        # 2. Simulem el POST amb el payload maliciós de l'apartat anterior
        payload = "hacker@test.com', is_superuser = true --"
        
        # Enviem l'atac a la URL d'actualitzar correu
        self.client.post(reverse('actualitzar_correu'), {'email': payload})

        # Tornem a carregar l'usuari de la base de dades per veure si ha canviat
        self.usuari.refresh_from_db()

        # 3. Assert: Comprovem si l'usuari s'ha convertit en superusuari.
        # El test "HA DE FALLAR" si volem demostrar que la vulnerabilitat existeix.
        # Per fer que el test doni FAIL quan detecta el forat, usem assertFalse.
        # Si és superuser sent un usuari normal, la seguretat ha fallat.
        self.assertFalse(self.usuari.is_superuser, "VULNERABILITAT DETECTADA: L'usuari ha escalat privilegis via SQLi!")