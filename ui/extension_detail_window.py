import tkinter as tk
from tkinter import ttk

class ExtensionDetailWindow:
    def __init__(self, parent, plugin, is_installed, dispatcher):
        self.parent = parent
        self.plugin = plugin
        self.is_installed = is_installed
        self.dispatcher = dispatcher
        self.detail_window = None
    
    def show_detail_window(self):
        """Affiche une fenêtre détaillée avec boutons d'action"""
        if self.detail_window:
            self.detail_window.destroy()
        
        # Créer la fenêtre de détails
        self.detail_window = tk.Toplevel(self.parent.root)
        self.detail_window.title(f"📦 {self.plugin['name']}")
        self.detail_window.geometry("600x500")
        self.detail_window.configure(bg='#0D1117')
        
        # Frame principal avec scroll
        main_frame = tk.Frame(self.detail_window, bg='#0D1117')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titre
        title_label = tk.Label(
            main_frame,
            text=f"📦 {self.plugin['name'].upper()}",
            font=('Arial', 16, 'bold'),
            fg='#FFD700',
            bg='#0D1117'
        )
        title_label.pack(pady=(0, 10))
        
        # Informations principales
        info_frame = tk.Frame(main_frame, bg='#2C3E50', relief='raised', bd=2)
        info_frame.pack(fill='x', pady=10)
        
        info_text = f"""
🏷️ Version: {self.plugin['version']}
👤 Auteur: {self.plugin['author']}
📂 Catégorie: {self.plugin['category']}
⭐ Note: {self.plugin['rating']}/5.0
📊 Téléchargements: {self.plugin['downloads']:,}
💾 Taille: {self.plugin['size']}

📝 Description:
{self.plugin['description']}

🏷️ Tags: {', '.join(self.plugin.get('tags', []))}
"""
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 10),
            fg='white',
            bg='#2C3E50',
            justify='left',
            anchor='nw'
        )
        info_label.pack(padx=15, pady=15)
        
        # Frame pour les boutons d'action
        action_frame = tk.Frame(main_frame, bg='#0D1117')
        action_frame.pack(fill='x', pady=20)
        
        if self.is_installed:
            # Boutons pour extension installée
            use_btn = tk.Button(
                action_frame,
                text=f"🔧 UTILISER {self.plugin['name']}",
                command=lambda: self.use_extension(),
                bg='#00AA00',
                fg='white',
                font=('Arial', 11, 'bold'),
                relief='raised',
                bd=3,
                padx=20,
                pady=8
            )
            use_btn.pack(side='left', padx=5)
            
            help_btn = tk.Button(
                action_frame,
                text="📖 AIDE",
                command=lambda: self.show_help(),
                bg='#0078D4',
                fg='white',
                font=('Arial', 11, 'bold'),
                relief='raised',
                bd=3,
                padx=20,
                pady=8
            )
            help_btn.pack(side='left', padx=5)
            
            remove_btn = tk.Button(
                action_frame,
                text="🗑️ DÉSINSTALLER",
                command=lambda: self.remove_extension(),
                bg='#CC0000',
                fg='white',
                font=('Arial', 11, 'bold'),
                relief='raised',
                bd=3,
                padx=20,
                pady=8
            )
            remove_btn.pack(side='right', padx=5)
        else:
            # Boutons pour extension non installée
            install_btn = tk.Button(
                action_frame,
                text=f"📥 INSTALLER {self.plugin['name']}",
                command=lambda: self.install_extension(),
                bg='#00AA00',
                fg='white',
                font=('Arial', 12, 'bold'),
                relief='raised',
                bd=3,
                padx=30,
                pady=10
            )
            install_btn.pack(side='left', padx=5)
        
        # Bouton README
        readme_btn = tk.Button(
            action_frame,
            text="📚 README",
            command=lambda: self.show_readme(),
            bg='#6B21A8',
            fg='white',
            font=('Arial', 11, 'bold'),
            relief='raised',
            bd=3,
            padx=20,
            pady=8
        )
        readme_btn.pack(side='left', padx=5)
        
        # Bouton fermer
        close_btn = tk.Button(
            main_frame,
            text="❌ FERMER",
            command=self.detail_window.destroy,
            bg='#7F1D1D',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='raised',
            bd=2
        )
        close_btn.pack(side='bottom', pady=10)
    
    def install_extension(self):
        """Installe l'extension"""
        result = self.dispatcher.plugin_manager.install_plugin(self.plugin['id'])
        self.parent.text_area.display_message(result)
        if result.startswith("✅"):
            self.detail_window.destroy()
    
    def remove_extension(self):
        """Désinstalle l'extension"""
        result = self.dispatcher.plugin_manager.remove_plugin(self.plugin['id'])
        self.parent.text_area.display_message(result)
        if result.startswith("✅"):
            self.detail_window.destroy()
    
    def use_extension(self):
        """Utilise l'extension"""
        command = f"ext {self.plugin['name']} help"
        self.parent.text_area.display_message(f"> {command}")
        result = self.dispatcher.process(command)
        self.parent.text_area.display_message(result)
        self.detail_window.destroy()
    
    def show_help(self):
        """Affiche l'aide de l'extension"""
        command = f"ext {self.plugin['name']} help"
        self.parent.text_area.display_message(f"> {command}")
        result = self.dispatcher.process(command)
        self.parent.text_area.display_message(result)
        self.detail_window.destroy()
    
    def show_readme(self):
        """Affiche le README de l'extension"""
        from ui.marketplace_tiles import MarketplaceTiles
        marketplace = MarketplaceTiles(self.parent, self.dispatcher)
        readme_content = marketplace.get_extension_readme(self.plugin['id'])
        
        readme_text = f"""
╔══════════════════════════════════════════════════════════════╗
║                    📚 README - {self.plugin['name'].upper()}                    ║
╚══════════════════════════════════════════════════════════════╝

{readme_content}

╔══════════════════════════════════════════════════════════════╗
║                        🎮 ACTIONS RAPIDES                   ║
╚══════════════════════════════════════════════════════════════╝
"""
        
        if self.is_installed:
            readme_text += f"""
🔧 UTILISER: ext {self.plugin['name']} help
📖 AIDE: ext {self.plugin['name']} help
"""
        else:
            readme_text += f"""
📥 INSTALLER: plugin install {self.plugin['id']}
"""
        
        self.parent.text_area.display_message(readme_text)
        self.detail_window.destroy()