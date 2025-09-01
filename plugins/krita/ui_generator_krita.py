#!/usr/bin/env python3
"""
Plugin Krita pour génération d'interfaces
Extension Docker intégrée
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from krita import *
from core.image_analyzer import ImageAnalyzer

class UIGeneratorDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 Générateur UI")
        self.analyzer = ImageAnalyzer()
        self.current_code = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurer l'interface du docker"""
        main_widget = QWidget()
        self.setWidget(main_widget)
        
        layout = QVBoxLayout(main_widget)
        
        # Titre
        title = QLabel("Générateur d'Interface")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin: 10px;")
        layout.addWidget(title)
        
        # Bouton analyser
        self.analyze_btn = QPushButton("🔍 Analyser l'image")
        self.analyze_btn.clicked.connect(self.analyze_current_image)
        layout.addWidget(self.analyze_btn)
        
        # Résultats
        results_group = QGroupBox("Éléments détectés")
        results_layout = QVBoxLayout(results_group)
        
        self.results_label = QLabel("Aucune analyse effectuée")
        self.results_label.setWordWrap(True)
        results_layout.addWidget(self.results_label)
        
        layout.addWidget(results_group)
        
        # Format de sortie
        format_group = QGroupBox("Format de sortie")
        format_layout = QVBoxLayout(format_group)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Tkinter (Python)", "PyQt5 (Python)", "HTML/CSS"])
        self.format_combo.currentIndexChanged.connect(self.on_format_changed)
        format_layout.addWidget(self.format_combo)
        
        layout.addWidget(format_group)
        
        # Code généré
        code_group = QGroupBox("Code généré")
        code_layout = QVBoxLayout(code_group)
        
        self.code_edit = QTextEdit()
        self.code_edit.setReadOnly(True)
        self.code_edit.setFont(QFont("Courier", 9))
        code_layout.addWidget(self.code_edit)
        
        layout.addWidget(code_group)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        copy_btn = QPushButton("📋 Copier")
        copy_btn.clicked.connect(self.copy_code)
        buttons_layout.addWidget(copy_btn)
        
        save_btn = QPushButton("💾 Sauver")
        save_btn.clicked.connect(self.save_code)
        buttons_layout.addWidget(save_btn)
        
        send_btn = QPushButton("📤 → CMD-AI")
        send_btn.clicked.connect(self.send_to_cmdai)
        buttons_layout.addWidget(send_btn)
        
        layout.addLayout(buttons_layout)
        
        # Stretch pour pousser vers le haut
        layout.addStretch()
    
    def analyze_current_image(self):
        """Analyser l'image active dans Krita"""
        try:
            # Obtenir le document actif
            app = Krita.instance()
            doc = app.activeDocument()
            
            if not doc:
                self.show_error("Aucun document ouvert dans Krita")
                return
            
            # Exporter temporairement
            temp_path = "/tmp/krita_ui_analysis.png"
            doc.exportImage(temp_path, InfoObject())
            
            # Analyser
            result = self.analyzer.analyze_image(temp_path)
            
            if "error" in result:
                self.show_error(result["error"])
                return
            
            # Afficher résultats
            elements_count = result["total_elements"]
            size = result["image_size"]
            
            result_text = f"✅ {elements_count} éléments détectés\n"
            result_text += f"📐 Taille: {size[0]}x{size[1]}px\n\n"
            
            for i, elem in enumerate(result["elements"]):
                result_text += f"{i+1}. {elem['type']} ({elem['x']},{elem['y']})\n"
            
            self.results_label.setText(result_text)
            
            # Générer code selon format
            self.generate_code_by_format()
            self.code_edit.setPlainText(self.current_code)
            
            # Renvoi automatique
            self.auto_send_to_cmdai()
            
            # Nettoyer
            os.remove(temp_path)
            
        except Exception as e:
            self.show_error(f"Erreur d'analyse: {str(e)}")
    
    def copy_code(self):
        """Copier le code"""
        if self.current_code:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.current_code)
            self.show_info("Code copié!")
    
    def save_code(self):
        """Sauvegarder le code"""
        if not self.current_code:
            self.show_error("Aucun code à sauvegarder")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder le code",
            "interface_generee.py",
            "Python files (*.py);;All files (*.*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.current_code)
                self.show_info(f"Code sauvegardé: {filename}")
            except Exception as e:
                self.show_error(f"Erreur: {str(e)}")
    
    def show_error(self, message):
        """Afficher erreur"""
        QMessageBox.critical(self, "Erreur", message)
    
    def show_info(self, message):
        """Afficher info"""
        QMessageBox.information(self, "Information", message)
    
    def generate_code_by_format(self):
        """Générer code selon format sélectionné"""
        format_index = self.format_combo.currentIndex()
        
        if format_index == 0:  # Tkinter
            self.current_code = self.analyzer.generate_tkinter_code()
        elif format_index == 1:  # PyQt5
            self.current_code = self.analyzer.generate_pyqt_code()
        elif format_index == 2:  # HTML
            self.current_code = self.analyzer.generate_html_code()
    
    def on_format_changed(self):
        """Changement de format"""
        if hasattr(self, 'analyzer') and self.analyzer.elements:
            self.generate_code_by_format()
            self.code_edit.setPlainText(self.current_code)
    
    def send_to_cmdai(self):
        """Envoyer vers CMD-AI"""
        if not self.current_code:
            self.show_error("Aucun code à envoyer")
            return
        
        try:
            import tempfile
            import subprocess
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(self.current_code)
                temp_path = f.name
            
            cmd_paths = ["/usr/local/bin/cmd-ai", "./main.py", "python main.py"]
            
            for cmd in cmd_paths:
                try:
                    subprocess.Popen([cmd, "--import", temp_path])
                    self.show_info("Code envoyé vers CMD-AI!")
                    return
                except:
                    continue
            
            self.show_error("CMD-AI non trouvé")
            
        except Exception as e:
            self.show_error(f"Erreur: {str(e)}")
    
    def auto_send_to_cmdai(self):
        """Renvoi automatique"""
        try:
            import os
            import time
            
            cmdai_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            output_dir = os.path.join(cmdai_dir, "user", "generated_interfaces")
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            filename = f"interface_{int(time.time())}.py"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.current_code)
            
        except:
            pass
    
    def canvasChanged(self, canvas):
        """Callback quand le canvas change"""
        pass

class UIGeneratorExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)
    
    def setup(self):
        """Configuration de l'extension"""
        pass
    
    def createActions(self, window):
        """Créer les actions du menu"""
        action = window.createAction("ui_generator", "Générateur UI", "tools/scripts")
        action.triggered.connect(self.show_docker)
    
    def show_docker(self):
        """Afficher le docker"""
        pass

# Enregistrement de l'extension
app = Krita.instance()
extension = UIGeneratorExtension(parent=app)
app.addExtension(extension)

# Enregistrement du docker
app.addDockWidgetFactory(DockWidgetFactory("ui_generator", DockWidgetFactoryBase.DockRight, UIGeneratorDocker))