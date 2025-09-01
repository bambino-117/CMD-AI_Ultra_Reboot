# Exemple d'utilisation des conteneurs avancés
if __name__ == "__main__":
    # Conteneur Blindé
    print("=== CONTENEUR BLINDÉ ===")
    
    conteneur_blinde = ConteneurBlinde("mon-super-code-secret")
    
    # Données sensibles à protéger
    donnees_sensibles = {
        "api_keys": ["key1", "key2", "key3"],
        "configurations": {"db_url": "mysql://user:pass@localhost"},
        "scripts": "print('Hello World')"
    }
    
    # Chargement avec code
    if conteneur_blinde.charger_contenu(donnees_sensibles, "mon-super-code-secret"):
        paquets = conteneur_blinde.obtenir_paquets()
        print(f"Nombre de paquets générés: {len(paquets)}")
        
        # Reconstruction (simulation)
        try:
            donnees_reconstruites = conteneur_blinde.reconstruire_contenu(
                "mon-super-code-secret", paquets
            )
            print("Reconstruction réussie!")
            print(f"Données: {donnees_reconstruites}")
        except Exception as e:
            print(f"Erreur reconstruction: {e}")
    
    # Conteneur Furtif
    print("\n=== CONTENEUR FURTIF ===")
    
    def condition_ouverture():
        # Exemple: n'ouvrir que sur certains systèmes
        return platform.system() == "Windows"
    
    conteneur_furtif = ConteneurFurtif(condition_ouverture)
    
    # Contenu à déployer
    contenu_deploiement = {
        "config.json": '{"auto_start": true, "silent_mode": true}',
        "module.py": "print('Module déployé avec succès')"
    }
    
    conteneur_furtif.charger_contenu(contenu_deploiement)
    
    if conteneur_furtif.ouvrir_conditionnel():
        try:
            emplacement = conteneur_furtif.deployer_automatique()
            print(f"Déployé avec succès à: {emplacement}")
        except Exception as e:
            print(f"Erreur déploiement: {e}")
    else:
        print("Conditions d'ouverture non remplies")