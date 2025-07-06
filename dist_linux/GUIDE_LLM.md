# Guide des Modèles IA - CMD-AI Ultra

## Modèles disponibles

### 1. ChatGPT (OpenAI)
- **Clé API**: Obtenir sur https://platform.openai.com/api-keys
- **Configuration**: `ext AIchat select 1` puis `ext AIchat apikey sk-...`
- **Modèle**: gpt-3.5-turbo

### 2. Gemini (Google)
- **Clé API**: Obtenir sur https://makersuite.google.com/app/apikey
- **Configuration**: `ext AIchat select 2` puis `ext AIchat apikey AIza...`
- **Modèle**: gemini-pro

### 3. Copilot (OpenAI GPT-4)
- **Clé API**: Même que ChatGPT
- **Configuration**: `ext AIchat select 3` puis `ext AIchat apikey sk-...`
- **Modèle**: gpt-4

### 4. DeepSeek
- **Clé API**: Obtenir sur https://platform.deepseek.com
- **Configuration**: `ext AIchat select 4` puis `ext AIchat apikey sk-...`
- **Modèle**: deepseek-chat

### 5. Ollama (Local)
- **Installation**: Voir INSTALL_OLLAMA.md
- **Configuration**: `ext AIchat select 5`
- **Gratuit et privé**

### 6. Mode Hors-ligne
- **Aucune configuration requise**
- **Réponses prédéfinies intelligentes**
- **Toujours disponible**

## Utilisation

```bash
# Configuration initiale
ext AIchat setup

# Sélectionner un modèle
ext AIchat select [1-6]

# Configurer clé API (si nécessaire)
ext AIchat apikey [votre_clé]

# Chatter
ext AIchat chat Bonjour !

# Voir l'historique
ext AIchat history

# Vérifier le statut
ext AIchat status
```

## Historique

L'historique des conversations est automatiquement sauvegardé dans `user/chat_history.json` et persiste entre les sessions.