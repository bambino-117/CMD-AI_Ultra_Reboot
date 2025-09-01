# 🔍 Guide OSINT avec CMD-AI Ultra Reboot

## Vue d'ensemble

L'extension OSINT de CMD-AI permet de faire de la recherche de renseignement en sources ouvertes (Open Source Intelligence) de manière éthique et légale.

## 🚀 Démarrage rapide

### 1. Activation de l'extension
```bash
# Accepter la décharge de responsabilité
ext OSINT disclaimer

# Activer l'extension
ext OSINT accept

# Lancer l'assistant guidé
ext OSINT wizard
```

### 2. Recherches de base

#### 📧 Recherche d'emails
```bash
# Rechercher des emails par domaine
ext OSINT email example.com
ext OSINT email startup.fr
ext OSINT email université.edu
```

#### 🌐 Analyse réseaux sociaux
```bash
# Vérifier la présence d'un username
ext OSINT social john_doe
ext OSINT social tech_guru
ext OSINT social startup_ceo
```

#### 🏢 Informations WHOIS/DNS
```bash
# Obtenir les infos d'un domaine
ext OSINT whois example.com
ext OSINT whois startup.io
ext OSINT whois blog.entreprise.fr
```

## 🔍 Techniques OSINT avancées

### Recherche par étapes

1. **Phase de reconnaissance**
   ```bash
   # Commencer par le domaine principal
   ext OSINT whois target-company.com
   
   # Rechercher les emails associés
   ext OSINT email target-company.com
   ```

2. **Analyse des personnes**
   ```bash
   # Rechercher les dirigeants sur les réseaux
   ext OSINT social ceo_username
   ext OSINT social cto_username
   ```

3. **Infrastructure technique**
   ```bash
   # Analyser les serveurs
   ext OSINT ip 93.184.216.34
   
   # Vérifier les archives
   ext OSINT archive https://target-company.com
   ```

### Corrélation des données

1. **Collecte multi-sources**
   - Combiner WHOIS + réseaux sociaux + archives
   - Croiser les informations obtenues
   - Vérifier la cohérence des données

2. **Timeline reconstruction**
   - Utiliser les archives pour l'historique
   - Corréler avec les dates WHOIS
   - Identifier les changements majeurs

## 📊 Génération de rapports

```bash
# Compiler tous les résultats
ext OSINT report "Investigation_Target_Company"

# Le rapport sera sauvé dans user/osint_reports/
```

## 🎯 Cas d'usage légitimes

### 1. **Audit de sécurité**
- Vérifier l'exposition d'informations sensibles
- Identifier les vecteurs d'attaque potentiels
- Évaluer la surface d'attaque

### 2. **Due diligence**
- Vérifier les informations d'une entreprise
- Analyser la présence en ligne
- Valider les contacts et dirigeants

### 3. **Investigation journalistique**
- Vérifier les sources et informations
- Recouper les déclarations publiques
- Identifier les connexions

### 4. **Recherche académique**
- Étudier les comportements en ligne
- Analyser les tendances
- Recherche en cybersécurité

## ⚠️ Limites et éthique

### Données accessibles
- **✅ Autorisé** : Données publiques, profils publics, archives web
- **❌ Interdit** : Données privées, contournement de protections

### Respect légal
- Conformité RGPD et lois locales
- Respect des conditions d'utilisation des sites
- Pas de collecte massive automatisée

### Usage éthique
- Pas de harcèlement ou stalking
- Respect de la vie privée
- Usage professionnel uniquement

## 🛠️ Outils complémentaires

### Intégration avec d'autres extensions
```bash
# Utiliser NetworkTools pour l'analyse technique
ext NetworkTools ping target-domain.com
ext NetworkTools scan target-ip

# Utiliser SystemMonitor pour l'analyse locale
ext SystemMonitor network
```

### Sauvegarde des résultats
- Rapports automatiques dans `user/osint_reports/`
- Export PDF et HTML
- Données JSON pour analyse ultérieure

## 🔒 Sécurité et confidentialité

### Protection des données
- Stockage local uniquement
- Pas de transmission vers des tiers
- Chiffrement des rapports sensibles

### Anonymisation
- Utilisation de proxies si nécessaire
- Rotation des User-Agents
- Respect des rate limits

## 📚 Ressources supplémentaires

### Formation OSINT
- Techniques de recherche avancées
- Outils spécialisés
- Méthodologies d'investigation

### Cadre légal
- Lois sur la vie privée
- Réglementations sectorielles
- Bonnes pratiques éthiques

---

**🔍 OSINT avec CMD-AI - Recherche intelligente et éthique !**