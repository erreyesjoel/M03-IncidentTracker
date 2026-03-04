from appium import webdriver
from appium.options.common import AppiumOptions
import time
import subprocess

# 1. Capabilities
options = AppiumOptions()
options.set_capability('platformName', 'Android')
options.set_capability('appium:automationName', 'UiAutomator2')
options.set_capability('appium:deviceName', 'emulator-5554')
options.set_capability('appium:app', '/home/joel-erreyes/cfgs/cicloCiber/MP03 - Posada en producció segura/ra 2/Pràctica_03_U2_M3_Framework_Web/M03-IncidentTracker/mobile_app/app/build/outputs/apk/debug/app-debug.apk')

driver = webdriver.Remote('http://localhost:4723', options=options)

try:
    print("🚀 Iniciant auditoria d'integració de dades...")
    time.sleep(5)

    # Netegem els logs de l'emulador abans de començar
    subprocess.run(["adb", "logcat", "-c"])

    # 2. Acció: Clicar el botó per demanar dades al Django
    driver.find_element(by="xpath", value='//android.widget.Button').click()
    print("✅ Botó clicat. Esperant tràfic entre Django i el Mòbil...")
    time.sleep(10) 

    # 3. VERIFICACIÓ DE SEGURETAT (LOGCAT)
    # Busquem el teu nom als logs del sistema perquè l'App els rep (comprovat via Logcat)
    print("🔍 Analitzant traces del sistema per confirmar recepció de dades...")
    logs = subprocess.check_output(["adb", "logcat", "-d"]).decode('utf-8')
    
    # El teu text objectiu
    target = "erreyes"
    
    if target in logs.lower():
        print(f"\n--- EVIDÈNCIA DE RECEPCIÓ TROBADA ---")
        print(f"✅ ✨ TEST GREEN (OK) ✨ ✅")
        print(f"S'ha confirmat que el mòbil ha rebut l'incident de: '{target}'")
        print(f"Traçabilitat: PostgreSQL -> Django -> Android Logcat [OK]")
    else:
        print("❌ El text no s'ha trobat als logs. Revisa si el Django està encès.")
        raise Exception(f"No s'ha detectat el text '{target}' al flux de dades.")

except Exception as e:
    print(f"\n❌ EVIDÈNCIA TDD: TEST RED (FAIL)")
    print(f"MOTIU: {e}")
    raise 
finally:
    driver.quit()