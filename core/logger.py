import logging
import os
from datetime import datetime

class AppLogger:
    def __init__(self, log_file="logs/app.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Configuration du logger
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()  # Console
            ]
        )
        
        self.logger = logging.getLogger('CMD-AI')
    
    def debug(self, message, context=""):
        self.logger.debug(f"[{context}] {message}")
    
    def info(self, message, context=""):
        self.logger.info(f"[{context}] {message}")
    
    def warning(self, message, context=""):
        self.logger.warning(f"[{context}] {message}")
    
    def error(self, message, context=""):
        self.logger.error(f"[{context}] {message}")
    
    def critical(self, message, context=""):
        self.logger.critical(f"[{context}] {message}")

# Instance globale
app_logger = AppLogger()