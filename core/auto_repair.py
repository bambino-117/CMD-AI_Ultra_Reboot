import os
import sys
import subprocess
import threading
import queue
import time
import json
from datetime import datetime
from core.logger import app_logger
from core.repair_notifications import get_repair_notification_manager

class RepairEngine:
    """Moteur de réparation automatique"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.repair_history = []
        
    def execute_repair(self, task):
        """Exécute une tâche de réparation"""
        try:
            repair_start = datetime.now()
            
            if task['type'] == 'dependency_fix':
                result = self._fix_dependencies(task['packages'])
            elif task['type'] == 'import_fix':
                result = self._fix_import_error(task['module'])
            elif task['type'] == 'file_repair':
                result = self._repair_file(task['filepath'])
            elif task['type'] == 'config_reset':
                result = self._reset_config(task['config_file'])
            elif task['type'] == 'cache_clean':
                result = self._clean_cache()
            else:
                result = {'success': False, 'error': f"Type de réparation inconnu: {task['type']}"}
            
            # Enregistrer l'historique
            repair_record = {
                'timestamp': repair_start.isoformat(),
                'task': task,
                'result': result,
                'duration': (datetime.now() - repair_start).total_seconds()
            }
            self.repair_history.append(repair_record)
            
            return result
            
        except Exception as e:
            app_logger.error(f"Erreur réparation: {e}", "AUTO_REPAIR")
            return {'success': False, 'error': str(e)}
    
    def _fix_dependencies(self, packages):
        """Répare les dépendances manquantes"""
        try:
            fixed_packages = []
            failed_packages = []
            
            for package in packages:
                try:
                    # Tentative d'installation silencieuse
                    result = subprocess.run([
                        sys.executable, '-m', 'pip', 'install', 
                        '--quiet', '--upgrade', package
                    ], capture_output=True, text=True, timeout=60)
                    
                    if result.returncode == 0:
                        fixed_packages.append(package)
                        app_logger.info(f"Package réparé: {package}", "AUTO_REPAIR")
                    else:
                        failed_packages.append(package)
                        
                except subprocess.TimeoutExpired:
                    failed_packages.append(package)
                except Exception as e:
                    failed_packages.append(package)
                    app_logger.warning(f"Échec réparation {package}: {e}", "AUTO_REPAIR")
            
            return {
                'success': len(fixed_packages) > 0,
                'fixed': fixed_packages,
                'failed': failed_packages,
                'message': f"Réparé: {len(fixed_packages)}, Échecs: {len(failed_packages)}"
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _fix_import_error(self, module_name):
        """Répare les erreurs d'import"""
        try:
            # Essayer d'importer le module
            try:
                __import__(module_name)
                return {'success': True, 'message': f"Module {module_name} déjà disponible"}
            except ImportError:
                pass
            
            # Tentative de réinstallation
            return self._fix_dependencies([module_name])
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _repair_file(self, filepath):
        """Répare un fichier corrompu"""
        try:
            if not os.path.exists(filepath):
                return {'success': False, 'error': f"Fichier non trouvé: {filepath}"}
            
            # Créer une sauvegarde
            backup_path = f"{filepath}.backup_{int(time.time())}"
            
            try:
                import shutil
                shutil.copy2(filepath, backup_path)
                
                # Vérifier l'intégrité du fichier
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Si le fichier est lisible, il n'est probablement pas corrompu
                return {
                    'success': True, 
                    'message': f"Fichier vérifié et sauvegardé: {backup_path}"
                }
                
            except Exception as e:
                # Tentative de restauration depuis backup si disponible
                backup_files = [f for f in os.listdir(os.path.dirname(filepath)) 
                               if f.startswith(os.path.basename(filepath) + '.backup_')]
                
                if backup_files:
                    latest_backup = max(backup_files)
                    backup_full_path = os.path.join(os.path.dirname(filepath), latest_backup)
                    shutil.copy2(backup_full_path, filepath)
                    return {'success': True, 'message': f"Fichier restauré depuis: {latest_backup}"}
                
                return {'success': False, 'error': f"Impossible de réparer: {e}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _reset_config(self, config_file):
        """Remet à zéro un fichier de configuration"""
        try:
            if not os.path.exists(config_file):
                return {'success': False, 'error': f"Fichier config non trouvé: {config_file}"}
            
            # Sauvegarde de la config actuelle
            backup_path = f"{config_file}.backup_{int(time.time())}"
            import shutil
            shutil.copy2(config_file, backup_path)
            
            # Configuration par défaut basique
            default_config = {
                "version": "2.0.0",
                "created": datetime.now().isoformat(),
                "auto_repair": True,
                "theme": "dark",
                "language": "fr"
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            
            return {
                'success': True, 
                'message': f"Configuration réinitialisée, sauvegarde: {backup_path}"
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _clean_cache(self):
        """Nettoie les caches système"""
        try:
            cleaned_items = []
            
            # Nettoyer cache Python
            cache_dirs = [
                '__pycache__',
                '.pytest_cache',
                'user/cache',
                'logs/temp'
            ]
            
            for cache_dir in cache_dirs:
                if os.path.exists(cache_dir):
                    try:
                        import shutil
                        shutil.rmtree(cache_dir)
                        cleaned_items.append(cache_dir)
                    except:
                        pass
            
            return {
                'success': True,
                'cleaned': cleaned_items,
                'message': f"Cache nettoyé: {len(cleaned_items)} éléments"
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

class BackgroundRepairWorker:
    """Worker de réparation en arrière-plan"""
    
    def __init__(self, config=None):
        self.task_queue = queue.PriorityQueue()
        self.engine = RepairEngine(config)
        self.active = False
        self.worker_thread = None
        self.repair_callbacks = []
        
    def start(self):
        """Démarre le worker en arrière-plan"""
        if self.active:
            return
        
        self.active = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        app_logger.info("Worker de réparation automatique démarré", "AUTO_REPAIR")
    
    def stop(self):
        """Arrête le worker"""
        self.active = False
        if self.worker_thread:
            self.worker_thread.join(timeout=2)
        app_logger.info("Worker de réparation automatique arrêté", "AUTO_REPAIR")
    
    def add_repair_task(self, task, priority=1):
        """Ajoute une tâche de réparation"""
        self.task_queue.put((priority, time.time(), task))
        app_logger.debug(f"Tâche de réparation ajoutée: {task['type']}", "AUTO_REPAIR")
    
    def add_callback(self, callback):
        """Ajoute un callback pour les résultats de réparation"""
        self.repair_callbacks.append(callback)
    
    def _worker_loop(self):
        """Boucle principale du worker"""
        while self.active:
            try:
                # Récupérer une tâche (timeout pour éviter le blocage)
                priority, timestamp, task = self.task_queue.get(timeout=1)
                
                # Exécuter la réparation
                result = self.engine.execute_repair(task)
                
                # Notifier les callbacks
                for callback in self.repair_callbacks:
                    try:
                        callback(task, result)
                    except Exception as e:
                        app_logger.warning(f"Erreur callback réparation: {e}", "AUTO_REPAIR")
                
                self.task_queue.task_done()
                
            except queue.Empty:
                # Pas de tâche, attendre un peu
                time.sleep(0.5)
            except Exception as e:
                app_logger.error(f"Erreur worker réparation: {e}", "AUTO_REPAIR")
                time.sleep(1)

class AutoRepairManager:
    """Gestionnaire principal de réparation automatique"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.worker = BackgroundRepairWorker(config)
        self.enabled = self.config.get('auto_repair_enabled', True)
        self.notification_callbacks = []
        self.notification_manager = get_repair_notification_manager()
        
        # Ajouter callback pour notifications
        self.worker.add_callback(self._on_repair_complete)
        
    def start(self):
        """Démarre le système de réparation automatique"""
        if self.enabled:
            self.worker.start()
            app_logger.info("Système de réparation automatique activé", "AUTO_REPAIR")
    
    def stop(self):
        """Arrête le système de réparation automatique"""
        self.worker.stop()
    
    def detect_and_repair(self, error_type, error_details):
        """Détecte et programme une réparation automatique"""
        if not self.enabled:
            return False
        
        # Notifier la détection
        self.notification_manager.notify_auto_detection(error_type, error_details)
        
        task = self._create_repair_task(error_type, error_details)
        if task:
            priority = self._get_priority(error_type)
            self.notification_manager.notify_repair_start(task)
            self.worker.add_repair_task(task, priority)
            return True
        
        return False
    
    def _create_repair_task(self, error_type, error_details):
        """Crée une tâche de réparation basée sur l'erreur"""
        if error_type == 'ImportError':
            module_name = error_details.get('module', '')
            if module_name:
                return {
                    'type': 'import_fix',
                    'module': module_name,
                    'description': f"Réparation import: {module_name}"
                }
        
        elif error_type == 'FileNotFoundError':
            filepath = error_details.get('filepath', '')
            if filepath:
                return {
                    'type': 'file_repair',
                    'filepath': filepath,
                    'description': f"Réparation fichier: {filepath}"
                }
        
        elif error_type == 'ConfigError':
            config_file = error_details.get('config_file', '')
            if config_file:
                return {
                    'type': 'config_reset',
                    'config_file': config_file,
                    'description': f"Reset configuration: {config_file}"
                }
        
        elif error_type == 'CacheError':
            return {
                'type': 'cache_clean',
                'description': "Nettoyage cache système"
            }
        
        return None
    
    def _get_priority(self, error_type):
        """Détermine la priorité de réparation"""
        priority_map = {
            'ImportError': 1,      # Haute priorité
            'ConfigError': 2,      # Moyenne priorité
            'FileNotFoundError': 3, # Basse priorité
            'CacheError': 4        # Très basse priorité
        }
        return priority_map.get(error_type, 5)
    
    def _on_repair_complete(self, task, result):
        """Callback appelé quand une réparation est terminée"""
        # Notifier via le gestionnaire de notifications
        self.notification_manager.notify_repair_complete(task, result)
        
        if result['success']:
            message = f"✅ Réparation réussie: {task['description']}"
            app_logger.info(message, "AUTO_REPAIR")
        else:
            message = f"❌ Échec réparation: {task['description']} - {result.get('error', 'Erreur inconnue')}"
            app_logger.warning(message, "AUTO_REPAIR")
        
        # Notifier les callbacks d'interface
        for callback in self.notification_callbacks:
            try:
                callback(task, result)
            except Exception as e:
                app_logger.warning(f"Erreur notification réparation: {e}", "AUTO_REPAIR")
    
    def add_notification_callback(self, callback):
        """Ajoute un callback pour les notifications d'interface"""
        self.notification_callbacks.append(callback)
    
    def get_repair_history(self):
        """Retourne l'historique des réparations"""
        return self.worker.engine.repair_history
    
    def manual_repair(self, repair_type, **kwargs):
        """Lance une réparation manuelle"""
        task = {
            'type': repair_type,
            'description': f"Réparation manuelle: {repair_type}",
            **kwargs
        }
        self.worker.add_repair_task(task, priority=0)  # Priorité maximale
        return "🔧 Réparation manuelle programmée"

# Instance globale du gestionnaire de réparation
auto_repair_manager = None

def initialize_auto_repair(config=None):
    """Initialise le système de réparation automatique"""
    global auto_repair_manager
    if auto_repair_manager is None:
        auto_repair_manager = AutoRepairManager(config)
        auto_repair_manager.start()
    return auto_repair_manager

def get_auto_repair_manager():
    """Retourne l'instance du gestionnaire de réparation"""
    global auto_repair_manager
    return auto_repair_manager

def auto_repair_decorator(func):
    """Décorateur pour capturer et réparer automatiquement les erreurs"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ImportError as e:
            if auto_repair_manager:
                auto_repair_manager.detect_and_repair('ImportError', {'module': str(e).split()[-1]})
            raise
        except FileNotFoundError as e:
            if auto_repair_manager:
                auto_repair_manager.detect_and_repair('FileNotFoundError', {'filepath': str(e)})
            raise
        except Exception as e:
            # Log l'erreur pour analyse future
            app_logger.error(f"Erreur capturée par auto-repair: {e}", "AUTO_REPAIR")
            raise
    
    return wrapper