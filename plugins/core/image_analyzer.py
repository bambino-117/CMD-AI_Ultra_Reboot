#!/usr/bin/env python3
"""
Analyseur d'images pour génération d'interfaces
Détecte les formes et génère du code Python
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import colorsys

class ImageAnalyzer:
    def __init__(self):
        self.elements = []
        self.image_size = (0, 0)
    
    def analyze_image(self, image_path):
        """Analyser une image et détecter les éléments d'interface"""
        img = cv2.imread(image_path)
        if img is None:
            return {"error": "Image non trouvée"}
        
        self.image_size = (img.shape[1], img.shape[0])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Détection des rectangles (boutons, champs)
        rectangles = self._detect_rectangles(gray)
        
        # Détection du texte
        text_regions = self._detect_text_regions(gray)
        
        # Classification des éléments
        self.elements = self._classify_elements(rectangles, text_regions)
        
        return {
            "elements": self.elements,
            "image_size": self.image_size,
            "total_elements": len(self.elements)
        }
    
    def _detect_rectangles(self, gray):
        """Détecter les rectangles avec analyse avancée"""
        # Détection multi-échelle
        rectangles = []
        
        # Canny avec plusieurs seuils
        for low, high in [(30, 100), (50, 150), (80, 200)]:
            edges = cv2.Canny(gray, low, high)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Approximation polygonale
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                if len(approx) == 4:  # Rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    if w > 15 and h > 8 and w < 800 and h < 600:
                        rectangles.append({
                            "x": int(x), "y": int(y),
                            "width": int(w), "height": int(h),
                            "area": w * h,
                            "aspect_ratio": w/h if h > 0 else 1,
                            "corners": len(approx)
                        })
        
        # Supprimer les doublons
        return self._remove_duplicate_rectangles(rectangles)
    
    def _detect_text_regions(self, gray):
        """Détecter les zones de texte"""
        text_regions = []
        
        # Détecter les zones avec beaucoup de contours fins (texte)
        kernel = np.ones((2,2), np.uint8)
        morph = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if 10 < w < 200 and 5 < h < 50:  # Taille typique du texte
                text_regions.append({
                    "x": int(x), "y": int(y),
                    "width": int(w), "height": int(h)
                })
        
        return text_regions
    
    def _classify_elements(self, rectangles, text_regions):
        """Classifier les éléments détectés"""
        elements = []
        
        for rect in rectangles:
            element_type = self._determine_element_type(rect, text_regions)
            
            elements.append({
                "type": element_type,
                "x": rect["x"],
                "y": rect["y"],
                "width": rect["width"],
                "height": rect["height"],
                "properties": self._get_element_properties(element_type, rect)
            })
        
        return elements
    
    def _determine_element_type(self, rect, text_regions):
        """Classification intelligente des éléments"""
        w, h = rect["width"], rect["height"]
        ratio = rect["aspect_ratio"]
        area = rect["area"]
        
        # Classification avancée
        if ratio > 4 and h < 35 and w > 80:
            return "entry"  # Champ de saisie long
        elif 1.5 < ratio < 4 and 20 < h < 50 and w > 50:
            return "button"  # Bouton standard
        elif ratio > 6 and h < 25:
            return "label"  # Label horizontal
        elif ratio < 1.5 and w > 100 and h > 100:
            return "frame"  # Conteneur carré
        elif h < 20:
            return "separator"  # Séparateur
        elif ratio > 8:
            return "progressbar"  # Barre de progression
        else:
            return "widget"  # Widget générique
    
    def _get_element_properties(self, element_type, rect):
        """Obtenir les propriétés par défaut d'un élément"""
        base_props = {
            "text": f"Element_{element_type}",
            "bg_color": "#E0E0E0",
            "fg_color": "#000000"
        }
        
        if element_type == "button":
            base_props.update({
                "text": "Button",
                "bg_color": "#D0D0D0",
                "relief": "raised"
            })
        elif element_type == "entry":
            base_props.update({
                "text": "",
                "bg_color": "#FFFFFF",
                "relief": "sunken"
            })
        elif element_type == "label":
            base_props.update({
                "text": "Label",
                "bg_color": "transparent"
            })
        
        return base_props
    
    def generate_tkinter_code(self):
        """Générer le code Tkinter"""
        if not self.elements:
            return "# Aucun élément détecté"
        
        code = f'''#!/usr/bin/env python3
import tkinter as tk

class GeneratedInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interface Générée")
        self.root.geometry("{self.image_size[0]}x{self.image_size[1]}")
        self.setup_ui()
    
    def setup_ui(self):'''
        
        for i, element in enumerate(self.elements):
            props = element["properties"]
            
            if element["type"] == "button":
                code += f'''
        btn_{i} = tk.Button(
            self.root,
            text="{props['text']}",
            bg="{props['bg_color']}",
            fg="{props['fg_color']}"
        )
        btn_{i}.place(x={element['x']}, y={element['y']}, width={element['width']}, height={element['height']})'''
            elif element["type"] == "entry":
                code += f'''
        entry_{i} = tk.Entry(
            self.root,
            bg="{props['bg_color']}",
            fg="{props['fg_color']}"
        )
        entry_{i}.place(x={element['x']}, y={element['y']}, width={element['width']}, height={element['height']})'''
            elif element["type"] == "label":
                code += f'''
        label_{i} = tk.Label(
            self.root,
            text="{props['text']}",
            bg="{props['bg_color']}",
            fg="{props['fg_color']}"
        )
        label_{i}.place(x={element['x']}, y={element['y']}, width={element['width']}, height={element['height']})'''
        
        code += '''

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GeneratedInterface()
    app.run()'''
        return code
    
    def _remove_duplicate_rectangles(self, rectangles):
        """Supprimer les rectangles en double"""
        unique = []
        for rect in rectangles:
            is_duplicate = False
            for existing in unique:
                if (abs(rect["x"] - existing["x"]) < 10 and 
                    abs(rect["y"] - existing["y"]) < 10 and
                    abs(rect["width"] - existing["width"]) < 20):
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique.append(rect)
        return unique
    
    def generate_pyqt_code(self):
        """Générer le code PyQt5"""
        if not self.elements:
            return "# Aucun élément détecté"
        
        code = f'''#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class GeneratedInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface Générée")
        self.setGeometry(100, 100, {self.image_size[0]}, {self.image_size[1]})
        self.setup_ui()
    
    def setup_ui(self):'''
        
        for i, element in enumerate(self.elements):
            props = element["properties"]
            
            if element["type"] == "button":
                code += f'''
        btn_{i} = QPushButton("{props['text']}", self)
        btn_{i}.setGeometry({element['x']}, {element['y']}, {element['width']}, {element['height']})
        btn_{i}.setStyleSheet("background-color: {props['bg_color']}; color: {props['fg_color']};")
        btn_{i}.clicked.connect(lambda: self.on_button_click("{props['text']}"))'''
            elif element["type"] == "entry":
                code += f'''
        entry_{i} = QLineEdit(self)
        entry_{i}.setGeometry({element['x']}, {element['y']}, {element['width']}, {element['height']})
        entry_{i}.setStyleSheet("background-color: {props['bg_color']}; color: {props['fg_color']};")
        entry_{i}.setPlaceholderText("Saisie...")'''
            elif element["type"] == "label":
                code += f'''
        label_{i} = QLabel("{props['text']}", self)
        label_{i}.setGeometry({element['x']}, {element['y']}, {element['width']}, {element['height']})
        label_{i}.setStyleSheet("color: {props['fg_color']};")'''
        
        code += '''
    
    def on_button_click(self, text):
        print(f"Bouton cliqué: {text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneratedInterface()
    window.show()
    sys.exit(app.exec_())'''
        return code
    
    def generate_html_code(self):
        """Générer le code HTML/CSS"""
        if not self.elements:
            return "<!-- Aucun élément détecté -->"
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Interface Générée</title>
    <style>
        body {{ margin: 0; padding: 0; width: {self.image_size[0]}px; height: {self.image_size[1]}px; position: relative; }}
        .element {{ position: absolute; }}
    </style>
</head>
<body>'''
        
        for i, element in enumerate(self.elements):
            props = element["properties"]
            
            if element["type"] == "button":
                html += f'''
    <button class="element" style="left: {element['x']}px; top: {element['y']}px; width: {element['width']}px; height: {element['height']}px; background-color: {props['bg_color']}; color: {props['fg_color']};">
        {props['text']}
    </button>'''
            elif element["type"] == "entry":
                html += f'''
    <input type="text" class="element" style="left: {element['x']}px; top: {element['y']}px; width: {element['width']}px; height: {element['height']}px; background-color: {props['bg_color']}; color: {props['fg_color']};" placeholder="Saisie...">'''
            elif element["type"] == "label":
                html += f'''
    <div class="element" style="left: {element['x']}px; top: {element['y']}px; width: {element['width']}px; height: {element['height']}px; color: {props['fg_color']};">
        {props['text']}
    </div>'''
        
        html += '''
</body>
</html>'''
        return html