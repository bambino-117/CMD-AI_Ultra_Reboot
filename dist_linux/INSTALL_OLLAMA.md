# Installation Ollama (Optionnel)

CMD-AI Ultra fonctionne sans installation supplémentaire avec le mode fallback.
Pour une expérience IA complète, vous pouvez installer Ollama.

## Installation rapide

### Linux/macOS
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
Télécharger depuis: https://ollama.ai/download

## Modèles recommandés (ultra légers)

```bash
# Modèle le plus léger (1.1GB)
ollama pull phi3:mini

# Alternative légère (1.3GB) 
ollama pull llama3.2:1b

# Pour du code (2.7GB)
ollama pull codellama:7b-code
```

## Démarrage

```bash
# Démarrer Ollama
ollama serve

# Dans un autre terminal, tester
ollama run phi3:mini
```

## Vérification

Relancez CMD-AI Ultra - il détectera automatiquement Ollama !

## Dépannage

- Port par défaut: 11434
- Logs: `ollama logs`
- Modèles installés: `ollama list`