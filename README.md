# 🤖 CMD-AI Ultra Reboot

**Application de chat/terminal IA modulaire et portable pour Windows/Linux**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/bambino-117/CMD-AI_Ultra_Reboot)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

## ✨ Fonctionnalités

### 🤖 **Intelligence Artificielle**
- **6 modèles IA** : OpenAI, Gemini, Ollama, Hugging Face, API personnalisées
- **Chat multimodal** : Texte + images avec capture d'écran intégrée
- **Mode hors-ligne** : Cache intelligent et réponses pré-définies
- **Conversations** : Sauvegarde, export PDF/HTML, gestion complète

### 🔌 **Marketplace d'Extensions**
- **9 extensions** : FileManager, NetworkTools, SystemMonitor, TextTools, Weather...
- **Interface style Empire** : Tuiles cliquables avec design Star Wars
- **Installation en 1 clic** : Boutons d'action intégrés
- **Documentation** : README et aide complète pour chaque extension

### 🎨 **Interface Avancée**
- **4 thèmes** : Clair, Sombre, Bleu, Vert avec application instantanée
- **Raccourcis clavier** : 7 raccourcis pour navigation rapide
- **Coloration syntaxique** : Code coloré dans les réponses
- **Capture d'écran** : Intégration native avec vignettes

### ⚙️ **Intégration Système**
- **Notifications natives** : Windows/macOS/Linux
- **Démarrage automatique** : Intégration OS complète
- **Menu contextuel** : Clic droit sur fichiers (Windows)
- **Monitoring système** : CPU, RAM, processus, températures

## 🚀 Installation Rapide

### **Prérequis**
```bash
Python 3.8+
pip (gestionnaire de paquets Python)
```

### **Installation**
```bash
# Cloner le projet
git clone https://github.com/bambino-117/CMD-AI_Ultra_Reboot.git
cd CMD-AI_Ultra_Reboot

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

### **Premier démarrage**
1. **Configuration IA** : Choisir un modèle (1-6)
2. **Clé API** : Ajouter votre clé si nécessaire
3. **Extensions** : Explorer le marketplace 🔌
4. **Personnalisation** : Changer le thème et paramètres

## 📦 Extensions Disponibles

| Extension | Description | Commandes |
|-----------|-------------|-----------|
| **🤖 AIchat** | Chat IA principal | `ext AIchat setup`, `ext AIchat chat [message]` |
| **📁 FileManager** | Gestion fichiers avancée | `ext FileManager search "*.pdf"`, `ext FileManager organize` |
| **🌐 NetworkTools** | Outils réseau complets | `ext NetworkTools ping google.com`, `ext NetworkTools speed` |
| **🖥️ SystemMonitor** | Monitoring système | `ext SystemMonitor status`, `ext SystemMonitor processes` |
| **🔤 TextTools** | Traitement de texte | `ext TextTools hash "text\|sha256"`, `ext TextTools regex` |
| **🌤️ Weather** | Météo et prévisions | `ext Weather current Paris`, `ext Weather forecast` |
| **📷 Screenshot** | Capture d'écran | `ext Screenshot take`, intégration native |

## ⌨️ Commandes Principales

### **🔌 Marketplace**
```bash
plugin list                    # Voir extensions disponibles
plugin install filemanager    # Installer une extension
plugin remove networktools    # Désinstaller une extension
```

### **💬 Conversations**
```bash
conv save "Ma conversation"    # Sauvegarder
conv list                      # Lister conversations
conv pdf "Ma conversation"     # Exporter en PDF
conv html "Ma conversation"    # Exporter en HTML
```

### **🎨 Interface**
```bash
theme list                     # Lister thèmes
theme set dark                 # Changer thème
theme toggle                   # Basculer clair/sombre
```

### **⚙️ Système**
```bash
system info                    # Informations système
system notify "Titre" "Msg"   # Notification test
cache status                   # Statut connexion
```

## 🎮 Raccourcis Clavier

| Raccourci | Action |
|-----------|--------|
| `Ctrl+Enter` | Envoyer message |
| `Ctrl+L` | Effacer saisie |
| `Ctrl+T` | Basculer thème |
| `Ctrl+Shift+S` | Capture d'écran |
| `Ctrl+S` | Sauvegarder conversation |
| `F1` | Aide |
| `Ctrl+Q` | Quitter |

## 🏗️ Architecture

```
CMD-AI_Ultra_Reboot/
├── main.py                 # Point d'entrée
├── core/                   # Logique métier
│   ├── dispatcher.py       # Gestionnaire principal
│   ├── theme_manager.py    # Gestion thèmes
│   ├── plugin_manager.py   # Marketplace
│   └── system_integration.py # Intégration OS
├── extensions/             # Extensions (9 disponibles)
├── language_models/        # Modèles IA (6 types)
├── ui/                     # Interface utilisateur
│   ├── interface.py        # Interface principale
│   ├── marketplace_tiles.py # Marketplace style Empire
│   └── widgets/            # Composants UI
├── ressources/             # Ressources statiques
└── user/                   # Configuration utilisateur
```

## 🔧 Configuration

### **Modèles IA Supportés**
1. **OpenAI GPT** (clé API requise)
2. **Google Gemini** (clé API requise)
3. **Ollama Local** (installation locale)
4. **Hugging Face** (clé API optionnelle)
5. **API Personnalisée** (configuration manuelle)
6. **Mode Simple** (réponses basiques)

### **Fichiers de Configuration**
- `user/config.json` - Configuration générale
- `user/api_keys.json` - Clés API (chiffré)
- `user/themes.json` - Thèmes personnalisés
- `user/conversations/` - Conversations sauvegardées

## 🌟 Fonctionnalités Avancées

### **Mode Hors-ligne Intelligent**
- Cache des réponses IA
- Patterns de réponses pré-définies
- Basculement automatique online/offline
- Statistiques de cache

### **Système de Plugins**
- Architecture modulaire BaseExtension
- Installation/désinstallation dynamique
- Marketplace en ligne avec mises à jour
- Extensions locales et distantes

### **Intégration OS Poussée**
- Notifications natives par plateforme
- Démarrage automatique (Registre/LaunchAgent/Autostart)
- Menu contextuel Windows
- Icône système avec menu

## 🐛 Dépannage

### **Problèmes Courants**
```bash
# Erreur d'import
pip install -r requirements.txt --upgrade

# Problème de permissions
python main.py --no-elevation

# Mode dégradé
# L'application démarre même si certains modules échouent
```

### **Logs**
```bash
# Consulter les logs
cat logs/cmd-ai.log

# Debug mode
python main.py --debug
```

## 🤝 Contribution

### **Développer une Extension**
```python
from core.base_extension import BaseExtension

class MonExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "MonExtension"
        self.version = "1.0.0"
    
    def execute(self, command, args=None):
        if command == "hello":
            return "Hello World!"
        return "Commande inconnue"
```

### **Ajouter au Marketplace**
1. Créer l'extension dans `/extensions/`
2. Ajouter l'entrée dans `marketplace.json`
3. Définir le README dans `get_extension_readme()`
4. Tester l'installation/désinstallation

## 📄 Licence

MIT License - Voir [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **OpenAI** pour l'API GPT
- **Google** pour Gemini
- **Ollama** pour les modèles locaux
- **Communauté Python** pour les bibliothèques
- **Testeurs** pour les retours et améliorations

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/bambino-117/CMD-AI_Ultra_Reboot/issues)
- **Documentation** : [Wiki](https://github.com/bambino-117/CMD-AI_Ultra_Reboot/wiki)
- **Discussions** : [GitHub Discussions](https://github.com/bambino-117/CMD-AI_Ultra_Reboot/discussions)

---

**🚀 CMD-AI Ultra Reboot - L'IA modulaire et extensible !**