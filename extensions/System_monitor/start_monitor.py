import subprocess
import sys
import os
import time

def start_system_monitor():
    try:
        # Chemin vers le script ancrage_sys_mon.py
        script_path = os.path.join(os.path.dirname(__file__), 'ancrage_sys_mon.py')
        
        # Démarrer le processus en arrière-plan
        process = subprocess.Popen([
            sys.executable, script_path
        ], creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
        
        print(f"System Monitor démarré avec PID: {process.pid}")
        return True
    except Exception as e:
        print(f"Erreur lors du démarrage: {e}")
        return False

if __name__ == "__main__":
    start_system_monitor()