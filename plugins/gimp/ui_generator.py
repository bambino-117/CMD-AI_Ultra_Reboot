#!/usr/bin/env python3
"""
Plugin GIMP pour génération d'interfaces
Fenêtre flottante qui analyse l'image active
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from gimpfu import *
import gtk
import gobject
from core.image_analyzer import ImageAnalyzer

class GimpUIGenerator:
    def __init__(self):
        self.window = None
        self.analyzer = ImageAnalyzer()
        self.current_code = ""
    
    def create_window(self):
        """Créer la fenêtre flottante"""
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("🎨 Générateur d'Interface")
        self.window.set_default_size(400, 600)
        self.window.set_resizable(True)
        
        # Layout principal
        vbox = gtk.VBox(False, 5)
        self.window.add(vbox)
        
        # Titre
        title = gtk.Label()
        title.set_markup("<b>Générateur d'Interface UI</b>")
        vbox.pack_start(title, False, False, 10)
        
        # Bouton analyser
        analyze_btn = gtk.Button("🔍 Analyser l'image")
        analyze_btn.connect("clicked", self.analyze_current_image)
        vbox.pack_start(analyze_btn, False, False, 5)
        
        # Zone de résultats
        results_frame = gtk.Frame("Éléments détectés")
        vbox.pack_start(results_frame, False, False, 5)
        
        self.results_label = gtk.Label("Aucune analyse effectuée")
        results_frame.add(self.results_label)
        
        # Zone de code
        code_frame = gtk.Frame("Code généré")
        vbox.pack_start(code_frame, True, True, 5)
        
        # Zone de texte avec scroll
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.code_view = gtk.TextView()
        self.code_view.set_editable(False)
        scrolled.add(self.code_view)
        code_frame.add(scrolled)
        
        # Sélecteur de format
        format_frame = gtk.Frame("Format de sortie")
        vbox.pack_start(format_frame, False, False, 5)
        
        format_combo = gtk.combo_box_new_text()
        format_combo.append_text("Tkinter (Python)")
        format_combo.append_text("PyQt5 (Python)")
        format_combo.append_text("HTML/CSS")
        format_combo.set_active(0)
        format_combo.connect("changed", self.on_format_changed)
        format_frame.add(format_combo)
        self.format_combo = format_combo
        
        # Boutons d'action
        hbox = gtk.HBox(True, 5)
        vbox.pack_start(hbox, False, False, 5)
        
        copy_btn = gtk.Button("📋 Copier")
        copy_btn.connect("clicked", self.copy_code)
        hbox.pack_start(copy_btn, True, True, 0)
        
        save_btn = gtk.Button("💾 Sauver")
        save_btn.connect("clicked", self.save_code)
        hbox.pack_start(save_btn, True, True, 0)
        
        send_btn = gtk.Button("📤 → CMD-AI")
        send_btn.connect("clicked", self.send_to_cmdai)
        hbox.pack_start(send_btn, True, True, 0)
        
        # Fermeture
        self.window.connect("delete-event", self.on_close)
        
        self.window.show_all()
    
    def analyze_current_image(self, widget):
        """Analyser l'image active dans GIMP"""
        try:
            # Obtenir l'image active
            image = gimp.image_list()[0] if gimp.image_list() else None
            if not image:
                self.show_error("Aucune image ouverte dans GIMP")
                return
            
            # Exporter temporairement l'image
            temp_path = "/tmp/gimp_ui_analysis.png"
            pdb.file_png_save(image, image.active_drawable, temp_path, temp_path, 0, 9, 0, 0, 0, 0, 0)
            
            # Analyser avec notre moteur
            result = self.analyzer.analyze_image(temp_path)
            
            if "error" in result:
                self.show_error(result["error"])
                return
            
            # Afficher les résultats
            elements_count = result["total_elements"]
            size = result["image_size"]
            
            result_text = f"✅ {elements_count} éléments détectés\n"
            result_text += f"📐 Taille: {size[0]}x{size[1]}px\n\n"
            
            for i, elem in enumerate(result["elements"]):
                result_text += f"{i+1}. {elem['type']} ({elem['x']},{elem['y']})\n"
            
            self.results_label.set_text(result_text)
            
            # Générer le code selon le format
            self.generate_code_by_format()
            
            # Afficher le code
            buffer = self.code_view.get_buffer()
            buffer.set_text(self.current_code)
            
            # Renvoi automatique vers CMD-AI
            self.auto_send_to_cmdai()
            
            # Nettoyer
            os.remove(temp_path)
            
        except Exception as e:
            self.show_error(f"Erreur d'analyse: {str(e)}")
    
    def copy_code(self, widget):
        """Copier le code dans le presse-papiers"""
        if self.current_code:
            clipboard = gtk.clipboard_get()
            clipboard.set_text(self.current_code)
            self.show_info("Code copié dans le presse-papiers!")
    
    def save_code(self, widget):
        """Sauvegarder le code dans un fichier"""
        if not self.current_code:
            self.show_error("Aucun code à sauvegarder")
            return
        
        dialog = gtk.FileChooserDialog(
            "Sauvegarder le code",
            self.window,
            gtk.FILE_CHOOSER_ACTION_SAVE,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
             gtk.STOCK_SAVE, gtk.RESPONSE_OK)
        )
        
        dialog.set_current_name("interface_generee.py")
        
        if dialog.run() == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.current_code)
                self.show_info(f"Code sauvegardé: {filename}")
            except Exception as e:
                self.show_error(f"Erreur sauvegarde: {str(e)}")
        
        dialog.destroy()
    
    def show_error(self, message):
        """Afficher un message d'erreur"""
        dialog = gtk.MessageDialog(
            self.window,
            gtk.DIALOG_MODAL,
            gtk.MESSAGE_ERROR,
            gtk.BUTTONS_OK,
            message
        )
        dialog.run()
        dialog.destroy()
    
    def show_info(self, message):
        """Afficher un message d'information"""
        dialog = gtk.MessageDialog(
            self.window,
            gtk.DIALOG_MODAL,
            gtk.MESSAGE_INFO,
            gtk.BUTTONS_OK,
            message
        )
        dialog.run()
        dialog.destroy()
    
    def generate_code_by_format(self):
        """Générer le code selon le format sélectionné"""
        format_index = self.format_combo.get_active()
        
        if format_index == 0:  # Tkinter
            self.current_code = self.analyzer.generate_tkinter_code()
        elif format_index == 1:  # PyQt5
            self.current_code = self.analyzer.generate_pyqt_code()
        elif format_index == 2:  # HTML
            self.current_code = self.analyzer.generate_html_code()
    
    def on_format_changed(self, combo):
        """Changement de format"""
        if hasattr(self, 'analyzer') and self.analyzer.elements:
            self.generate_code_by_format()
            buffer = self.code_view.get_buffer()
            buffer.set_text(self.current_code)
    
    def send_to_cmdai(self, widget):
        """Envoyer le code vers CMD-AI"""
        if not self.current_code:
            self.show_error("Aucun code à envoyer")
            return
        
        try:
            import tempfile
            import subprocess
            
            # Créer fichier temporaire
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(self.current_code)
                temp_path = f.name
            
            # Essayer de lancer CMD-AI
            cmd_paths = [
                "/usr/local/bin/cmd-ai",
                "./main.py",
                "python main.py"
            ]
            
            for cmd in cmd_paths:
                try:
                    subprocess.Popen([cmd, "--import", temp_path])
                    self.show_info("Code envoyé vers CMD-AI!")
                    return
                except:
                    continue
            
            self.show_error("CMD-AI non trouvé")
            
        except Exception as e:
            self.show_error(f"Erreur envoi: {str(e)}")
    
    def auto_send_to_cmdai(self):
        """Renvoi automatique vers CMD-AI"""
        try:
            import os
            import tempfile
            
            # Créer fichier dans le dossier CMD-AI
            cmdai_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            output_dir = os.path.join(cmdai_dir, "user", "generated_interfaces")
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Sauvegarder automatiquement
            import time
            filename = f"interface_{int(time.time())}.py"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.current_code)
            
            self.show_info(f"Code sauvé: {filename}")
            
        except Exception as e:
            pass  # Échec silencieux
    
    def on_close(self, widget, event):
        """Fermer la fenêtre"""
        self.window.hide()
        return True

# Instance globale
ui_generator = None

def launch_ui_generator():
    """Lancer le générateur d'interface"""
    global ui_generator
    
    if ui_generator is None:
        ui_generator = GimpUIGenerator()
    
    ui_generator.create_window()

# Enregistrement du plugin GIMP
register(
    "python_fu_ui_generator",
    "Générateur d'Interface UI",
    "Analyse l'image et génère du code d'interface Python",
    "CMD-AI Ultra Reboot",
    "CMD-AI Ultra Reboot",
    "2024",
    "<Image>/Tools/UI Generator...",
    "*",
    [],
    [],
    launch_ui_generator
)

main()