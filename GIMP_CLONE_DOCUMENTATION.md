# 🎨 GIMP Clone Studio - Documentation

## Vue d'ensemble

GIMP Clone Studio est un éditeur d'interface visuel inspiré de GIMP qui génère automatiquement du code pour différents frameworks. Il combine la puissance d'un éditeur graphique avec la génération de code automatique.

## 🏗️ Architecture

### Structure principale
```
GimpCloneStudio/
├── Interface GIMP-like
│   ├── Barre de menu
│   ├── Barre d'outils principale
│   ├── Panneau gauche (Outils + Couleurs)
│   ├── Zone centrale (Canvas + Éditeur de code)
│   └── Panneau droit (Calques + Propriétés)
└── Génération de code
    ├── Templates pour différents langages
    ├── Génération automatique
    └── Prévisualisation en temps réel
```

## 🛠️ Fonctionnalités

### Interface utilisateur
- **Boîte à outils** : Rectangle, Ellipse, Texte, Bouton, Champ de saisie, etc.
- **Système de calques** : Comme GIMP, avec visibilité et organisation
- **Palette de couleurs** : Avant-plan/Arrière-plan + couleurs rapides
- **Propriétés** : Modification en temps réel des éléments

### Génération de code
- **Tkinter** : Code Python avec widgets Tkinter
- **PyQt5** : Interface PyQt (en développement)
- **HTML/CSS** : Pages web responsives (en développement)
- **Flutter** : Applications mobiles (en développement)

## 🚀 Utilisation

### Lancement depuis CMD-AI
```bash
# Méthodes de lancement
gimp launch          # Lance l'interface
designer             # Raccourci
gimp help            # Aide détaillée
```

### Workflow typique
1. **Dessiner** : Utilisez les outils pour créer votre interface
2. **Organiser** : Gérez les calques pour structurer
3. **Ajuster** : Modifiez les propriétés dans le panneau droit
4. **Générer** : Le code est généré automatiquement
5. **Prévisualiser** : Testez votre interface
6. **Exporter** : Sauvegardez le code généré

## 💻 Code généré

### Exemple Tkinter
```python
#!/usr/bin/env python3
import tkinter as tk

class GeneratedInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interface Générée")
        self.root.geometry("800x600")
        
        # Bouton à (100, 50)
        button_0 = tk.Button(self.root, text="Button",
                           width=10, height=2,
                           bg="#E0E0E0")
        button_0.place(x=100, y=50)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GeneratedInterface()
    app.run()
```

## 🎨 Outils disponibles

### Widgets de base
- **Rectangle** → `tk.Frame` avec bordures
- **Ellipse** → Forme ovale décorative
- **Bouton** → `tk.Button`
- **Texte** → `tk.Label`
- **Champ de saisie** → `tk.Entry`

### Widgets avancés
- **Case à cocher** → `tk.Checkbutton`
- **Bouton radio** → `tk.Radiobutton`
- **Liste** → `tk.Listbox`
- **Barre de progression** → `ttk.Progressbar`
- **Onglets** → `ttk.Notebook`

## ⚙️ Configuration

### Couleurs
- **Avant-plan** : Couleur principale (texte, bordures)
- **Arrière-plan** : Couleur de fond
- **Palette rapide** : 8 couleurs prédéfinies

### Options d'outil
- **Taille** : Épaisseur des bordures (1-20px)
- **Style** : solid, dashed, dotted
- **Propriétés** : Position (X,Y) et taille (W,H)

## 📂 Gestion de projet

### Sauvegarde
- **Format** : `.gimp` (JSON structuré)
- **Contenu** : Éléments, calques, paramètres
- **Compatibilité** : Rechargeable et modifiable

### Export
- **Code source** : Fichiers prêts à l'emploi
- **Multiple formats** : `.py`, `.html`, `.dart`
- **Prévisualisation** : Test en temps réel

## 🔧 Intégration CMD-AI

### Commandes disponibles
```bash
gimp launch          # Lance l'éditeur
gimp help            # Aide complète
designer             # Raccourci rapide
```

### Messages d'aide
- Guide d'installation si fichiers manquants
- Messages d'erreur détaillés
- Suggestions de solutions

## 🚀 Roadmap

### Version actuelle (v1.0)
- ✅ Interface GIMP-like complète
- ✅ Génération code Tkinter
- ✅ Système de calques
- ✅ Outils de base

### Prochaines versions
- 🔄 Support PyQt5 complet
- 🔄 Génération HTML/CSS
- 🔄 Widgets personnalisés
- 🔄 Thèmes d'interface
- 🔄 Plugin system
- 🔄 Collaboration temps réel

### Fonctionnalités avancées prévues
- 📋 Copier/Coller entre projets
- 🔍 Recherche d'éléments
- 📏 Guides et grilles
- 🎯 Alignement automatique
- 📱 Responsive design
- 🌐 Export vers différents frameworks

## 🐛 Résolution de problèmes

### Erreurs communes
1. **Interface ne s'ouvre pas**
   - Vérifier que `gimp_clone_studio.py` existe
   - Relancer avec `gimp install`

2. **Code généré incorrect**
   - Vérifier les propriétés des éléments
   - Régénérer avec le bouton "🔄 Générer"

3. **Prévisualisation échoue**
   - Vérifier la syntaxe du code
   - Sauvegarder avant de prévisualiser

### Support
- Tapez `gimp help` pour l'aide intégrée
- Vérifiez les logs dans la console
- Redémarrez l'application si nécessaire

## 📖 Exemples d'usage

### Interface simple
1. Rectangle → Frame principal
2. Bouton → Action principale
3. Champ texte → Saisie utilisateur
4. Export → Code prêt à l'emploi

### Interface complexe
1. Plusieurs calques pour organisation
2. Widgets imbriqués
3. Système de navigation
4. Gestion des événements

---

**GIMP Clone Studio** - Créez des interfaces visuellement, obtenez du code automatiquement ! 🎨✨
