#!/usr/bin/env python3
"""
Pont d'intégration entre extensions et fonctionnalités principales
"""

import json
from pathlib import Path
from typing import Dict, List, Any

class ExtensionBridge:
    def __init__(self):
        self.bridges = {}
        self.active_connections = {}
        self.integration_config = Path("user/extension_integrations.json")
        self.load_integrations()
    
    def load_integrations(self):
        """Charge les configurations d'intégration"""
        if self.integration_config.exists():
            with open(self.integration_config, 'r') as f:
                self.bridges = json.load(f)
        else:
            self.create_default_integrations()
    
    def create_default_integrations(self):
        """Crée les intégrations par défaut entre extensions"""
        self.bridges = {
            "aichat_security": {
                "description": "Intégration IA avec outils sécurité",
                "connections": [
                    {"from": "AIchat", "to": "SecurityToolkit", "trigger": "security_analysis"},
                    {"from": "AIchat", "to": "OSINTExtension", "trigger": "investigate"},
                    {"from": "SecurityToolkit", "to": "AIchat", "trigger": "report_findings"}
                ]
            },
            "system_monitoring": {
                "description": "Surveillance système avec IA",
                "connections": [
                    {"from": "SystemMonitor", "to": "AIchat", "trigger": "anomaly_detected"},
                    {"from": "SystemMonitor", "to": "SecurityToolkit", "trigger": "security_alert"}
                ]
            },
            "file_security": {
                "description": "Analyse sécurité des fichiers",
                "connections": [
                    {"from": "FileManager", "to": "SecurityToolkit", "trigger": "scan_file"},
                    {"from": "SecurityToolkit", "to": "FileManager", "trigger": "quarantine_file"}
                ]
            },
            "network_analysis": {
                "description": "Analyse réseau avec OSINT",
                "connections": [
                    {"from": "NetworkTools", "to": "OSINTExtension", "trigger": "analyze_ip"},
                    {"from": "OSINTExtension", "to": "SecurityToolkit", "trigger": "threat_detected"}
                ]
            },
            "usb_security": {
                "description": "Sécurité USB avec BadUSB",
                "connections": [
                    {"from": "USBManager", "to": "BadUSBCreator", "trigger": "create_payload"},
                    {"from": "USBManager", "to": "SecurityToolkit", "trigger": "scan_usb"}
                ]
            }
        }
        self.save_integrations()
    
    def save_integrations(self):
        """Sauvegarde les configurations d'intégration"""
        self.integration_config.parent.mkdir(exist_ok=True)
        with open(self.integration_config, 'w') as f:
            json.dump(self.bridges, f, indent=2)
    
    def register_extension_hook(self, extension_name: str, hook_name: str, callback):
        """Enregistre un hook d'extension"""
        if extension_name not in self.active_connections:
            self.active_connections[extension_name] = {}
        self.active_connections[extension_name][hook_name] = callback
    
    def trigger_bridge(self, from_ext: str, trigger: str, data: Any = None):
        """Déclenche une liaison entre extensions"""
        results = []
        
        for bridge_name, bridge_config in self.bridges.items():
            for connection in bridge_config["connections"]:
                if connection["from"] == from_ext and connection["trigger"] == trigger:
                    to_ext = connection["to"]
                    
                    # Exécuter la liaison
                    result = self.execute_bridge(from_ext, to_ext, trigger, data)
                    if result:
                        results.append({
                            "bridge": bridge_name,
                            "from": from_ext,
                            "to": to_ext,
                            "result": result
                        })
        
        return results
    
    def execute_bridge(self, from_ext: str, to_ext: str, trigger: str, data: Any):
        """Exécute une liaison spécifique"""
        if to_ext in self.active_connections:
            hooks = self.active_connections[to_ext]
            if trigger in hooks:
                try:
                    return hooks[trigger](data)
                except Exception as e:
                    return f"Erreur liaison {from_ext}->{to_ext}: {e}"
        
        return f"Liaison {from_ext}->{to_ext} non disponible"
    
    def get_available_bridges(self) -> Dict:
        """Retourne les liaisons disponibles"""
        return {
            name: {
                "description": config["description"],
                "connections": len(config["connections"]),
                "active": any(
                    conn["to"] in self.active_connections 
                    for conn in config["connections"]
                )
            }
            for name, config in self.bridges.items()
        }
    
    def create_smart_workflow(self, workflow_name: str, steps: List[Dict]):
        """Crée un workflow intelligent entre extensions"""
        workflow = {
            "name": workflow_name,
            "steps": steps,
            "created": Path(__file__).stat().st_mtime
        }
        
        # Sauvegarder le workflow
        workflows_file = Path("user/smart_workflows.json")
        workflows = {}
        
        if workflows_file.exists():
            with open(workflows_file, 'r') as f:
                workflows = json.load(f)
        
        workflows[workflow_name] = workflow
        
        workflows_file.parent.mkdir(exist_ok=True)
        with open(workflows_file, 'w') as f:
            json.dump(workflows, f, indent=2)
        
        return workflow
    
    def suggest_integrations(self, extension_name: str) -> List[str]:
        """Suggère des intégrations pour une extension"""
        suggestions = []
        
        integration_map = {
            "AIchat": [
                "Analysez les fichiers suspects avec SecurityToolkit",
                "Recherchez des informations avec OSINTExtension",
                "Surveillez le système avec SystemMonitor"
            ],
            "SecurityToolkit": [
                "Analysez les résultats avec AIchat",
                "Scannez les fichiers avec FileManager",
                "Vérifiez les connexions avec NetworkTools"
            ],
            "OSINTExtension": [
                "Analysez les IPs avec NetworkTools",
                "Rapportez à AIchat pour analyse",
                "Alertez SecurityToolkit si menace"
            ],
            "FileManager": [
                "Scannez les fichiers avec SecurityToolkit",
                "Analysez le contenu avec AIchat",
                "Surveillez les modifications avec SystemMonitor"
            ],
            "NetworkTools": [
                "Analysez les IPs avec OSINTExtension",
                "Rapportez les anomalies à SecurityToolkit",
                "Surveillez le trafic avec SystemMonitor"
            ]
        }
        
        return integration_map.get(extension_name, [
            "Intégrez avec AIchat pour l'analyse",
            "Connectez avec SecurityToolkit pour la sécurité",
            "Utilisez SystemMonitor pour la surveillance"
        ])

# Exemples d'utilisation des liaisons
class IntegrationExamples:
    def __init__(self, bridge: ExtensionBridge):
        self.bridge = bridge
    
    def setup_security_workflow(self):
        """Configure un workflow de sécurité complet"""
        workflow_steps = [
            {
                "step": 1,
                "extension": "SystemMonitor",
                "action": "scan_system",
                "description": "Scanner le système"
            },
            {
                "step": 2,
                "extension": "SecurityToolkit",
                "action": "analyze_threats",
                "description": "Analyser les menaces"
            },
            {
                "step": 3,
                "extension": "AIchat",
                "action": "generate_report",
                "description": "Générer un rapport IA"
            },
            {
                "step": 4,
                "extension": "OSINTExtension",
                "action": "investigate_threats",
                "description": "Enquête OSINT sur les menaces"
            }
        ]
        
        return self.bridge.create_smart_workflow("security_analysis", workflow_steps)
    
    def setup_file_analysis_workflow(self):
        """Configure un workflow d'analyse de fichiers"""
        workflow_steps = [
            {
                "step": 1,
                "extension": "FileManager",
                "action": "select_files",
                "description": "Sélectionner les fichiers"
            },
            {
                "step": 2,
                "extension": "SecurityToolkit",
                "action": "scan_files",
                "description": "Scanner les fichiers"
            },
            {
                "step": 3,
                "extension": "AIchat",
                "action": "analyze_content",
                "description": "Analyser le contenu"
            }
        ]
        
        return self.bridge.create_smart_workflow("file_analysis", workflow_steps)

def main():
    print("🔗 Configuration des liaisons entre extensions...")
    
    bridge = ExtensionBridge()
    examples = IntegrationExamples(bridge)
    
    # Créer les workflows par défaut
    security_workflow = examples.setup_security_workflow()
    file_workflow = examples.setup_file_analysis_workflow()
    
    print("✅ Liaisons configurées:")
    for name, info in bridge.get_available_bridges().items():
        print(f"  • {name}: {info['description']} ({info['connections']} connexions)")
    
    print(f"\n✅ Workflows créés:")
    print(f"  • {security_workflow['name']}: {len(security_workflow['steps'])} étapes")
    print(f"  • {file_workflow['name']}: {len(file_workflow['steps'])} étapes")
    
    print("\n🎉 Système de liaisons configuré avec succès !")

if __name__ == "__main__":
    main()