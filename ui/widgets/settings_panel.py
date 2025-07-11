import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import platform
from core.user_manager import UserManager
from core.system_detector import SystemDetector
from core.system_report import SystemReport
from core.kaamelott_responses import KaamelottResponses
from language_models.llm_manager import LLMManager
from ui.widgets.placeholder_entry import PlaceholderEntry
from ui.widgets.simple_pseudo_editor import SimplePseudoEditor
from ui.widgets.custom_button import create_button

class SettingsPanel:
    def __init__(self, parent):
        self.parent = parent
        self.user_manager = UserManager()
        self.system_detector = SystemDetector()
        self.llm_manager = LLMManager()
        
        # Frame principal
        self.frame = ttk.LabelFrame(parent, text="⚙️ Paramètres", padding="10", width=400)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Nettoyer le frame avant de recréer
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # 1. Pseudo éditable
        pseudo_frame = ttk.Frame(self.frame)
        pseudo_frame.pack(fill='x', pady=5)
        
        self.pseudo_editor = SimplePseudoEditor(pseudo_frame)
        self.pseudo_editor.pack(side='left')
        
        # 2. API Keys
        api_frame = ttk.LabelFrame(self.frame, text="🔑 Clés API", padding="5")
        api_frame.pack(fill='x', pady=10)
        
        api_keys = self.user_manager.settings.get('api_keys', {})
        
        # OpenAI
        openai_frame = ttk.Frame(api_frame)
        openai_frame.pack(fill='x', pady=2)
        ttk.Label(openai_frame, text="OpenAI:", width=10).pack(side='left')
        self.openai_var = tk.StringVar(value=api_keys.get('openai', ''))
        openai_entry = PlaceholderEntry(openai_frame, placeholder="sk-...", textvariable=self.openai_var, show='*', width=25)
        openai_entry.pack(side='left', padx=5)
        create_button(openai_frame, "Sauver", lambda: self.save_api_key('openai'), width=8, symbol="💾").pack(side='left')
        
        # Gemini
        gemini_frame = ttk.Frame(api_frame)
        gemini_frame.pack(fill='x', pady=2)
        ttk.Label(gemini_frame, text="Gemini:", width=10).pack(side='left')
        self.gemini_var = tk.StringVar(value=api_keys.get('gemini', ''))
        gemini_entry = PlaceholderEntry(gemini_frame, placeholder="AIza...", textvariable=self.gemini_var, show='*', width=25)
        gemini_entry.pack(side='left', padx=5)
        create_button(gemini_frame, "Sauver", lambda: self.save_api_key('gemini'), width=8, symbol="💾").pack(side='left')
        
        # DeepSeek
        deepseek_frame = ttk.Frame(api_frame)
        deepseek_frame.pack(fill='x', pady=2)
        ttk.Label(deepseek_frame, text="DeepSeek:", width=10).pack(side='left')
        self.deepseek_var = tk.StringVar(value=api_keys.get('deepseek', ''))
        deepseek_entry = PlaceholderEntry(deepseek_frame, placeholder="sk-...", textvariable=self.deepseek_var, show='*', width=25)
        deepseek_entry.pack(side='left', padx=5)
        create_button(deepseek_frame, "Sauver", lambda: self.save_api_key('deepseek'), width=8, symbol="💾").pack(side='left')
        
        # 3. Extensions
        ext_frame = ttk.LabelFrame(self.frame, text="🧩 Extensions", padding="5")
        ext_frame.pack(fill='x', pady=10)
        
        # AIchat status
        aichat_frame = ttk.Frame(ext_frame)
        aichat_frame.pack(fill='x', pady=2)
        ttk.Label(aichat_frame, text="🤖 AIchat:").pack(side='left')
        
        current_model = self.llm_manager.get_current_model_info()
        model_text = current_model['name'] if current_model else "Non configuré"
        ttk.Label(aichat_frame, text=model_text, foreground='green').pack(side='left', padx=10)
        
        create_button(aichat_frame, "Config", self.config_aichat, width=8, symbol="⚙️").pack(side='right')
        
        # Extension Screenshot
        screenshot_frame = ttk.Frame(ext_frame)
        screenshot_frame.pack(fill='x', pady=2)
        ttk.Label(screenshot_frame, text="📸 Screenshot:").pack(side='left')
        
        from core.daily_suggestions import DailySuggestions
        daily_suggestions = DailySuggestions()
        
        if daily_suggestions.is_screenshot_installed():
            ttk.Label(screenshot_frame, text="Installée", foreground='green').pack(side='left', padx=10)
            create_button(screenshot_frame, "Test", self.test_screenshot, width=8, symbol="📷").pack(side='right')
        else:
            ttk.Label(screenshot_frame, text="Non installée", foreground='orange').pack(side='left', padx=10)
            create_button(screenshot_frame, "Installer", self.install_screenshot, width=8, symbol="📥").pack(side='right')
        
        # 4. Fichiers et dossiers
        file_frame = ttk.LabelFrame(self.frame, text="📁 Fichiers", padding="5")
        file_frame.pack(fill='x', pady=10)
        
        # Première ligne - Dossiers
        folder_btn_frame = ttk.Frame(file_frame)
        folder_btn_frame.pack(fill='x', pady=2)
        
        create_button(folder_btn_frame, "Dossier User", self.open_user_folder, width=10, symbol="📁").pack(side='left')
        create_button(folder_btn_frame, "Logs", self.open_logs_folder, width=8, symbol="📋").pack(side='left', padx=(5,0))
        create_button(folder_btn_frame, "Config", self.open_config_folder, width=8, symbol="⚙️").pack(side='left', padx=(5,0))
        
        # Deuxième ligne - Actions
        action_btn_frame = ttk.Frame(file_frame)
        action_btn_frame.pack(fill='x', pady=2)
        
        create_button(action_btn_frame, "Rapport Système", self.generate_report, width=12, symbol="📄").pack(side='left')
        create_button(action_btn_frame, "Erreurs", self.view_error_reports, width=8, symbol="🚨").pack(side='left', padx=(5,0))
        create_button(action_btn_frame, "Effacer Tout", self.clear_history, width=10, symbol="🗑️").pack(side='left', padx=(5,0))
    
    def open_user_folder(self):
        """Ouvre le dossier user contenant les données utilisateur"""
        user_path = os.path.abspath("user")
        os.makedirs(user_path, exist_ok=True)
        
        try:
            if platform.system() == "Windows":
                os.startfile(user_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", user_path])
            else:  # Linux
                subprocess.run(["xdg-open", user_path])
            messagebox.showinfo("📁", f"Dossier user ouvert !\n\nContient :\n• Configurations\n• Conversations\n• Rapports d'erreurs\n• Screenshots\n• Cache")
        except Exception as e:
            messagebox.showerror("❌", f"Erreur ouverture dossier: {e}")
    
    def open_logs_folder(self):
        """Ouvre le dossier des logs"""
        logs_path = os.path.abspath("logs")
        os.makedirs(logs_path, exist_ok=True)
        
        try:
            if platform.system() == "Windows":
                os.startfile(logs_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", logs_path])
            else:  # Linux
                subprocess.run(["xdg-open", logs_path])
        except Exception as e:
            messagebox.showerror("❌", f"Erreur ouverture logs: {e}")
    
    def open_config_folder(self):
        """Ouvre le dossier racine de l'application"""
        config_path = os.path.abspath(".")
        
        try:
            if platform.system() == "Windows":
                os.startfile(config_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", config_path])
            else:  # Linux
                subprocess.run(["xdg-open", config_path])
        except Exception as e:
            messagebox.showerror("❌", f"Erreur ouverture config: {e}")
    
    def view_error_reports(self):
        """Affiche les rapports d'erreurs"""
        error_file = "user/error_reports.txt"
        
        if not os.path.exists(error_file):
            messagebox.showinfo("✅", "Aucun rapport d'erreur trouvé !\n\nL'application fonctionne correctement.")
            return
        
        try:
            # Créer une fenêtre pour afficher les erreurs
            error_window = tk.Toplevel(self.parent)
            error_window.title("🚨 Rapports d'Erreurs")
            error_window.geometry("600x400")
            
            # Zone de texte avec scrollbar
            text_frame = ttk.Frame(error_window)
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame, wrap='word')
            scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            # Lire et afficher les erreurs
            with open(error_file, 'r', encoding='utf-8') as f:
                content = f.read()
                text_widget.insert('1.0', content)
            
            text_widget.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Boutons
            btn_frame = ttk.Frame(error_window)
            btn_frame.pack(fill='x', padx=10, pady=5)
            
            create_button(btn_frame, "Effacer Erreurs", lambda: self.clear_error_reports(error_window), symbol="🗑️").pack(side='left')
            create_button(btn_frame, "Fermer", error_window.destroy, symbol="❌").pack(side='right')
            
        except Exception as e:
            messagebox.showerror("❌", f"Erreur lecture rapports: {e}")
    
    def clear_error_reports(self, window=None):
        """Efface les rapports d'erreurs"""
        error_file = "user/error_reports.txt"
        
        try:
            if os.path.exists(error_file):
                os.remove(error_file)
            messagebox.showinfo("✅", "Rapports d'erreurs effacés !")
            if window:
                window.destroy()
        except Exception as e:
            messagebox.showerror("❌", f"Erreur effacement: {e}")
    
    def generate_report(self):
        try:
            report = SystemReport()
            report_path = report.save_report()
            messagebox.showinfo("✅", f"Rapport généré: {report_path}\n\n{KaamelottResponses.get_encouragement()}")
        except Exception as e:
            messagebox.showerror("❌", f"Erreur génération rapport: {e}\n\n{KaamelottResponses.get_error()}")
    
    def clear_history(self):
        """Efface toutes les données personnelles"""
        result = messagebox.askyesno("⚠️ Confirmation", 
                                    "Effacer TOUTES les données personnelles ?\n\n• Historique conversations\n• Clés API\n• Configuration utilisateur\n• Logs\n\nCette action est irréversible !")
        
        if result:
            try:
                import shutil
                
                # Fichiers à supprimer
                files_to_delete = [
                    'user/settings.json',
                    'user/installation.json',
                    'user/rapport_systeme.md',
                    'user/error_reports.txt'
                ]
                
                # Dossiers à vider
                dirs_to_clear = [
                    'logs/',
                    'user/conversations/',
                    'user/cache/',
                    'user/session_reports/',
                    'user/github_reports/',
                    'user/screenshots/'
                ]
                
                deleted_count = 0
                
                # Supprimer fichiers
                for file_path in files_to_delete:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        deleted_count += 1
                
                # Vider dossiers
                for dir_path in dirs_to_clear:
                    if os.path.exists(dir_path):
                        shutil.rmtree(dir_path)
                        os.makedirs(dir_path, exist_ok=True)
                        deleted_count += 1
                
                messagebox.showinfo("✅", f"Historique effacé !\n{deleted_count} éléments supprimés.\n\n⚠️ Redémarrez l'application pour appliquer les changements.")
                
            except Exception as e:
                messagebox.showerror("❌", f"Erreur lors de l'effacement: {e}")
    
    def save_api_key(self, provider):
        if provider == 'openai':
            key = self.openai_var.get().strip()
        elif provider == 'gemini':
            key = self.gemini_var.get().strip()
        elif provider == 'deepseek':
            key = self.deepseek_var.get().strip()
        
        if key:
            self.llm_manager.configure_api_key(provider, key)
            messagebox.showinfo("✅", f"Clé {provider} sauvegardée !\n\n{KaamelottResponses.get_encouragement()}")
        else:
            messagebox.showwarning("⚠️", f"Clé vide !\n\n{KaamelottResponses.get_impatience()}")
    
    def config_aichat(self):
        # Ouvrir une fenêtre de config AIchat
        config_window = tk.Toplevel(self.parent)
        config_window.title("🤖 Configuration AIchat")
        config_window.geometry("400x300")
        config_window.resizable(False, False)
        
        # Menu de sélection
        menu_text = self.llm_manager.get_model_selection_menu()
        text_widget = tk.Text(config_window, wrap='word', height=15)
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', menu_text)
        text_widget.config(state='disabled')
        
        # Frame boutons
        btn_frame = ttk.Frame(config_window)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        for i in range(1, 7):
            create_button(btn_frame, str(i), lambda x=i: self.select_model(x, config_window), width=4).pack(side='left', padx=2)
    
    def select_model(self, model_num, window):
        if self.llm_manager.switch_model_by_number(str(model_num)):
            messagebox.showinfo("✅", f"Modèle {model_num} activé !\n\n{KaamelottResponses.get_encouragement()}")
            window.destroy()
            self.setup_ui()
        else:
            messagebox.showerror("❌", f"Erreur activation modèle {model_num}\n\n{KaamelottResponses.get_error()}")
    
    def install_screenshot(self):
        """Installe l'extension Screenshot"""
        try:
            from core.daily_suggestions import DailySuggestions
            daily_suggestions = DailySuggestions()
            result = daily_suggestions.install_screenshot()
            messagebox.showinfo("✅", f"{result}\n\n{KaamelottResponses.get_encouragement()}")
            self.setup_ui()  # Rafraîchir l'interface
        except Exception as e:
            messagebox.showerror("❌", f"Erreur installation Screenshot: {e}\n\n{KaamelottResponses.get_error()}")
    
    def test_screenshot(self):
        """Teste l'extension Screenshot"""
        try:
            from extensions.screenshot_extension import ScreenshotExtension
            screenshot_ext = ScreenshotExtension()
            result = screenshot_ext.show_help("")
            messagebox.showinfo("📸 Screenshot", result)
        except Exception as e:
            messagebox.showerror("❌", f"Erreur test Screenshot: {e}\n\n{KaamelottResponses.get_error()}")
    
    def show(self):
        self.frame.pack(side='left', fill='y', padx=10, pady=10)
        self.frame.pack_propagate(False)  # Maintenir la largeur fixée
    
    def hide(self):
        self.frame.pack_forget()