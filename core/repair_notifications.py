import time
from datetime import datetime
from core.logger import app_logger

class RepairNotificationManager:
    """Gestionnaire de notifications pour les réparations automatiques"""
    
    def __init__(self):
        self.notifications = []
        self.max_notifications = 50
        self.ui_callbacks = []
    
    def add_ui_callback(self, callback):
        """Ajoute un callback pour l'interface utilisateur"""
        self.ui_callbacks.append(callback)
    
    def notify_repair_start(self, task):
        """Notifie le début d'une réparation"""
        notification = {
            'type': 'repair_start',
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'message': f"🔧 Début réparation: {task['description']}"
        }
        self._add_notification(notification)
    
    def notify_repair_complete(self, task, result):
        """Notifie la fin d'une réparation"""
        if result['success']:
            icon = "✅"
            message = f"Réparation réussie: {task['description']}"
            if 'message' in result:
                message += f" - {result['message']}"
        else:
            icon = "❌"
            message = f"Échec réparation: {task['description']}"
            if 'error' in result:
                message += f" - {result['error']}"
        
        notification = {
            'type': 'repair_complete',
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'result': result,
            'message': f"{icon} {message}"
        }
        self._add_notification(notification)
        
        # Notifier l'interface utilisateur
        self._notify_ui(notification)
    
    def notify_auto_detection(self, error_type, error_details):
        """Notifie la détection automatique d'un problème"""
        notification = {
            'type': 'auto_detection',
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type,
            'error_details': error_details,
            'message': f"🔍 Problème détecté: {error_type}"
        }
        self._add_notification(notification)
    
    def get_recent_notifications(self, count=10):
        """Retourne les notifications récentes"""
        return self.notifications[-count:] if self.notifications else []
    
    def get_notification_summary(self):
        """Retourne un résumé des notifications"""
        if not self.notifications:
            return "📭 Aucune notification de réparation"
        
        recent = self.get_recent_notifications(5)
        summary = "🔔 NOTIFICATIONS RÉCENTES\n\n"
        
        for notif in reversed(recent):
            timestamp = notif['timestamp'][:19].replace('T', ' ')
            summary += f"{timestamp}\n{notif['message']}\n\n"
        
        return summary
    
    def _add_notification(self, notification):
        """Ajoute une notification à la liste"""
        self.notifications.append(notification)
        
        # Limiter le nombre de notifications
        if len(self.notifications) > self.max_notifications:
            self.notifications = self.notifications[-self.max_notifications:]
        
        app_logger.info(notification['message'], "REPAIR_NOTIF")
    
    def _notify_ui(self, notification):
        """Notifie l'interface utilisateur"""
        for callback in self.ui_callbacks:
            try:
                callback(notification)
            except Exception as e:
                app_logger.warning(f"Erreur callback UI notification: {e}", "REPAIR_NOTIF")

# Instance globale
repair_notification_manager = RepairNotificationManager()

def get_repair_notification_manager():
    """Retourne l'instance du gestionnaire de notifications"""
    return repair_notification_manager