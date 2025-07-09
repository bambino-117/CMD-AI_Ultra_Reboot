# 🔌 Plugins Éditeurs d'Images

Plugins pour GIMP, Krita et Photoshop qui analysent les images et génèrent du code d'interface Python.

## 📁 Structure

```
plugins/
├── gimp/                    # Plugin GIMP (Python-Fu)
├── krita/                   # Plugin Krita (Python)
├── photoshop/               # Plugin Photoshop (CEP)
├── core/                    # Logique commune
└── shared/                  # Ressources partagées
```

## 🎯 Fonctionnalités

- **Analyse d'image** : Détection automatique des formes
- **Reconnaissance** : Boutons, champs, labels, frames
- **Génération** : Code Tkinter/PyQt/HTML prêt à l'emploi
- **Interface** : Fenêtre flottante dans l'éditeur

## 🚀 Installation

Chaque plugin s'installe dans son éditeur respectif et communique avec le moteur d'analyse central.