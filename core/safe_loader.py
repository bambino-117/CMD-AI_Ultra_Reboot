import traceback
import sys

class SafeLoader:
    def __init__(self):
        self.failed_modules = []
        self.fallback_mode = False
    
    def safe_import(self, module_name, fallback=None):
        """Import sécurisé avec fallback"""
        try:
            return __import__(module_name)
        except Exception as e:
            print(f"Échec import {module_name}: {e}")
            self.failed_modules.append(module_name)
            return fallback
    
    def safe_execute(self, func, *args, fallback_result=None, context=""):
        """Exécution sécurisée avec fallback"""
        try:
            return func(*args)
        except Exception as e:
            print(f"Erreur {context}: {e}")
            if self.fallback_mode:
                return fallback_result
            raise
    
    def safe_class_init(self, cls, *args, fallback_class=None, **kwargs):
        """Initialisation sécurisée de classe"""
        try:
            return cls(*args, **kwargs)
        except Exception as e:
            print(f"Échec initialisation {cls.__name__}: {e}")
            if fallback_class:
                try:
                    return fallback_class(*args, **kwargs)
                except:
                    pass
            return None
    
    def enable_fallback_mode(self):
        """Active le mode dégradé"""
        self.fallback_mode = True
        print("Mode dégradé activé")
    
    def get_failed_modules(self):
        """Retourne la liste des modules qui ont échoué"""
        return self.failed_modules