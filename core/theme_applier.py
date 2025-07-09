#!/usr/bin/env python3
"""
Applicateur de thèmes en temps réel
"""

import tkinter as tk
from tkinter import ttk
import json
import os

class ThemeApplier:
    def __init__(self, root_window):
        self.root = root_window
        self.current_theme_data = None
        
    def apply_theme_immediately(self, theme_data):
        """Applique un thème immédiatement à l'interface"""
        self.current_theme_data = theme_data
        
        try:
            # Appliquer à la fenêtre principale
            if 'bg_color' in theme_data:
                self.root.configure(bg=theme_data['bg_color'])
            
            # Appliquer récursivement à tous les widgets
            self._apply_to_widget_tree(self.root, theme_data)
            
            # Forcer la mise à jour
            self.root.update_idletasks()
            
            return True
        except Exception as e:
            print(f"Erreur application thème: {e}")
            return False
    
    def _apply_to_widget_tree(self, widget, theme_data):
        """Applique le thème récursivement à tous les widgets"""
        try:
            widget_class = widget.winfo_class()
            
            # Configuration selon le type de widget
            if widget_class == "Tk":  # Fenêtre principale
                widget.configure(bg=theme_data.get('bg_color', '#FFFFFF'))
            
            elif widget_class == "Frame":
                widget.configure(bg=theme_data.get('bg_color', '#FFFFFF'))
            
            elif widget_class == "Label":
                widget.configure(
                    bg=theme_data.get('bg_color', '#FFFFFF'),
                    fg=theme_data.get('text_color', '#000000')
                )
            
            elif widget_class == "Button":
                widget.configure(
                    bg=theme_data.get('button_bg', '#E0E0E0'),
                    fg=theme_data.get('button_fg', '#000000'),
                    activebackground=theme_data.get('accent_color', '#0078D4'),
                    activeforeground=theme_data.get('bg_color', '#FFFFFF')
                )
            
            elif widget_class == "Entry":
                widget.configure(
                    bg=theme_data.get('input_bg', '#FFFFFF'),
                    fg=theme_data.get('text_color', '#000000'),
                    insertbackground=theme_data.get('accent_color', '#0078D4')
                )
            
            elif widget_class == "Text":
                widget.configure(
                    bg=theme_data.get('input_bg', '#FFFFFF'),
                    fg=theme_data.get('text_color', '#000000'),
                    insertbackground=theme_data.get('accent_color', '#0078D4'),
                    selectbackground=theme_data.get('accent_color', '#0078D4'),
                    selectforeground=theme_data.get('bg_color', '#FFFFFF')
                )
            
            elif widget_class == "Listbox":
                widget.configure(
                    bg=theme_data.get('input_bg', '#FFFFFF'),
                    fg=theme_data.get('text_color', '#000000'),
                    selectbackground=theme_data.get('accent_color', '#0078D4'),
                    selectforeground=theme_data.get('bg_color', '#FFFFFF')
                )
            
            elif widget_class == "Canvas":
                widget.configure(bg=theme_data.get('input_bg', '#FFFFFF'))
            
            # Widgets TTK
            elif isinstance(widget, ttk.Widget):
                self._apply_ttk_theme(widget, theme_data)
            
        except Exception as e:
            pass  # Ignorer les erreurs de widgets spécifiques
        
        # Appliquer aux widgets enfants
        try:
            for child in widget.winfo_children():
                self._apply_to_widget_tree(child, theme_data)
        except:
            pass
    
    def _apply_ttk_theme(self, widget, theme_data):
        """Applique le thème aux widgets TTK"""
        try:
            style = ttk.Style()
            
            # Configurer les styles TTK selon le thème
            if theme_data.get('name') == 'Néon Bleu':
                self._configure_neon_ttk_style(style, theme_data)
            else:
                self._configure_standard_ttk_style(style, theme_data)
                
        except Exception as e:
            pass
    
    def _configure_neon_ttk_style(self, style, theme_data):
        """Configure le style TTK pour le thème néon"""
        style.theme_use('clam')
        
        # Boutons néon
        style.configure("Neon.TButton",
            background=theme_data.get('button_bg', '#001122'),
            foreground=theme_data.get('button_fg', '#00BFFF'),
            borderwidth=theme_data.get('border_width', 1),
            focuscolor="none",
            relief="flat"
        )
        
        style.map("Neon.TButton",
            background=[('active', theme_data.get('accent_color', '#00FFFF')),
                       ('pressed', theme_data.get('border_color', '#00BFFF'))],
            foreground=[('active', theme_data.get('bg_color', '#0A0A0A')),
                       ('pressed', theme_data.get('bg_color', '#0A0A0A'))]
        )
        
        # Appliquer le style néon aux boutons TTK
        for widget in self._find_ttk_widgets(self.root, ttk.Button):
            widget.configure(style="Neon.TButton")
    
    def _configure_standard_ttk_style(self, style, theme_data):
        """Configure le style TTK standard"""
        style.configure("TButton",
            background=theme_data.get('button_bg', '#E0E0E0'),
            foreground=theme_data.get('button_fg', '#000000')
        )
        
        style.configure("TEntry",
            fieldbackground=theme_data.get('input_bg', '#FFFFFF'),
            foreground=theme_data.get('text_color', '#000000')
        )
        
        style.configure("TLabel",
            background=theme_data.get('bg_color', '#FFFFFF'),
            foreground=theme_data.get('text_color', '#000000')
        )
    
    def _find_ttk_widgets(self, parent, widget_type):
        """Trouve tous les widgets TTK d'un type donné"""
        widgets = []
        
        def search_recursive(widget):
            if isinstance(widget, widget_type):
                widgets.append(widget)
            try:
                for child in widget.winfo_children():
                    search_recursive(child)
            except:
                pass
        
        search_recursive(parent)
        return widgets

# Instance globale pour l'application
_theme_applier_instance = None

def get_theme_applier(root_window=None):
    """Récupère l'instance du theme applier"""
    global _theme_applier_instance
    if _theme_applier_instance is None and root_window:
        _theme_applier_instance = ThemeApplier(root_window)
    return _theme_applier_instance

def apply_theme_to_interface(theme_data, root_window=None):
    """Fonction utilitaire pour appliquer un thème"""
    applier = get_theme_applier(root_window)
    if applier:
        return applier.apply_theme_immediately(theme_data)
    return False