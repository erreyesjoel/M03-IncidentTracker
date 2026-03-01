from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import os
import time

class SecurityRegressionTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        
        # RUTA CRÍTICA PER A UBUNTU SNAP:
        # Intentem usar la ruta interna de snap que permet l'execució binària directa
        snap_path = "/snap/firefox/current/usr/lib/firefox/firefox"
        if os.path.exists(snap_path):
            opts.binary_location = snap_path
        else:
            # Si no existeix la ruta 'current', apuntem a la de l'usuari (fallback)
            opts.binary_location = "/usr/bin/firefox"

        try:
            # Deixem que Selenium Manager gestioni el geckodriver automàticament
            # Assegura't de tenir instal·lat: pip install selenium --upgrade
            cls.selenium = WebDriver(options=opts)
            cls.selenium.implicitly_wait(10)
        except Exception as e:
            print(f"ERROR CRÍTIC INICIALITZANT SELENIUM: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        # Només tanquem si s'ha arribat a crear la instància
        if hasattr(cls, 'selenium'):
            cls.selenium.quit()
        super().tearDownClass()

    def test_role_restriction(self):
        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
        # 1. Anar a la pàgina de login
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))

        # 2. Emplenar dades de l'analista1
        # Comprova que al teu testdb.json l'usuari es digui exactament així
        self.selenium.find_element(By.NAME, "username").send_keys("analista1")
        self.selenium.find_element(By.NAME, "password").send_keys("Alumne2025-")
        
        # 3. Clicar el botó de login
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # Esperem un segon perquè el servidor processi el login i la sessió
        time.sleep(1)

        # 4. Intentar forçar l'entrada a l'URL d'administració
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))

        # 5. ASSERT (Fase RED):
        # A l'Evidència 2, aquest test HA DE FALLAR (F) perquè l'analista és staff al JSON.
        # Això demostrarà que hi ha una vulnerabilitat o mala configuració de rols.
        self.assertNotEqual(
            self.selenium.title, 
            "Site administration | Django site admin", 
            "SEGURETAT FALLIDA (RED): L'analista ha pogut accedir al panell d'administració!"
        )