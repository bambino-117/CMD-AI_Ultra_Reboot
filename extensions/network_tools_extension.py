from core.base_extension import BaseExtension
import subprocess
import socket
import requests
import json
from datetime import datetime

class NetworkToolsExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "NetworkTools"
        self.version = "1.2.0"
        self.description = "Outils réseau: ping, scan ports, vitesse, géolocalisation IP"
        self.author = "CMD-AI Team"
    
    def initialize(self, app_context):
        self.app_context = app_context
    
    def execute(self, command, args=None):
        if command == "ping":
            return self.ping_host(args)
        elif command == "scan":
            return self.scan_ports(args)
        elif command == "speed":
            return self.test_speed()
        elif command == "ip":
            return self.get_ip_info(args)
        elif command == "wifi":
            return self.scan_wifi()
        elif command == "help":
            return self.show_help()
        else:
            return "Commandes: ping, scan, speed, ip, wifi, help"
    
    def ping_host(self, host=None):
        """Ping un hôte"""
        if not host:
            host = "google.com"
        
        try:
            import platform
            param = "-n" if platform.system().lower() == "windows" else "-c"
            
            result = subprocess.run(
                ["ping", param, "4", host],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                # Extraire les statistiques
                stats = [line for line in lines if 'time=' in line or 'temps=' in line]
                
                response = f"🌐 PING {host}\n\n"
                if stats:
                    response += "📊 Résultats:\n"
                    for stat in stats[:4]:
                        response += f"   {stat.strip()}\n"
                else:
                    response += "✅ Hôte accessible\n"
                
                return response
            else:
                return f"❌ Impossible de joindre {host}"
                
        except Exception as e:
            return f"❌ Erreur ping: {e}"
    
    def scan_ports(self, target=None):
        """Scan des ports ouverts"""
        if not target:
            target = "127.0.0.1"
        
        try:
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306]
            open_ports = []
            
            for port in common_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                
                try:
                    result = sock.connect_ex((target, port))
                    if result == 0:
                        open_ports.append(port)
                except:
                    pass
                finally:
                    sock.close()
            
            if open_ports:
                result = f"🔍 SCAN PORTS - {target}\n\n"
                result += "🟢 Ports ouverts:\n"
                
                port_services = {
                    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
                    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
                    443: "HTTPS", 993: "IMAPS", 995: "POP3S",
                    3389: "RDP", 5432: "PostgreSQL", 3306: "MySQL"
                }
                
                for port in open_ports:
                    service = port_services.get(port, "Inconnu")
                    result += f"   • {port} ({service})\n"
                
                return result
            else:
                return f"🔍 Aucun port ouvert trouvé sur {target}"
                
        except Exception as e:
            return f"❌ Erreur scan: {e}"
    
    def test_speed(self):
        """Test de vitesse réseau"""
        try:
            # Test simple de latence
            start_time = datetime.now()
            response = requests.get("https://httpbin.org/status/200", timeout=5)
            end_time = datetime.now()
            
            latency = (end_time - start_time).total_seconds() * 1000
            
            # Test de téléchargement simple
            start_time = datetime.now()
            response = requests.get("https://httpbin.org/bytes/1024", timeout=10)
            end_time = datetime.now()
            
            download_time = (end_time - start_time).total_seconds()
            speed_kbps = (1024 / download_time) / 1024 if download_time > 0 else 0
            
            result = f"🚀 TEST DE VITESSE\n\n"
            result += f"📡 Latence: {latency:.1f} ms\n"
            result += f"⬇️ Vitesse: ~{speed_kbps:.1f} MB/s (test simple)\n"
            result += f"🌐 Connexion: {'✅ Stable' if latency < 100 else '⚠️ Lente'}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur test vitesse: {e}"
    
    def get_ip_info(self, ip=None):
        """Informations sur une IP"""
        try:
            if not ip:
                # Obtenir IP publique
                response = requests.get("https://httpbin.org/ip", timeout=5)
                ip = response.json().get("origin", "").split(",")[0]
            
            # Informations géographiques (service gratuit)
            try:
                geo_response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                geo_data = geo_response.json()
                
                if geo_data.get("status") == "success":
                    result = f"🌍 INFORMATIONS IP: {ip}\n\n"
                    result += f"📍 Pays: {geo_data.get('country', 'N/A')}\n"
                    result += f"🏙️ Ville: {geo_data.get('city', 'N/A')}\n"
                    result += f"🏢 FAI: {geo_data.get('isp', 'N/A')}\n"
                    result += f"🕐 Timezone: {geo_data.get('timezone', 'N/A')}\n"
                    
                    return result
                else:
                    return f"🌐 IP: {ip}\n⚠️ Informations géographiques non disponibles"
                    
            except:
                return f"🌐 IP: {ip}\n⚠️ Service de géolocalisation indisponible"
                
        except Exception as e:
            return f"❌ Erreur info IP: {e}"
    
    def scan_wifi(self):
        """Scan des réseaux WiFi (Linux/macOS)"""
        try:
            import platform
            system = platform.system()
            
            if system == "Linux":
                result = subprocess.run(
                    ["nmcli", "dev", "wifi", "list"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')[1:11]  # 10 premiers réseaux
                    
                    response = "📶 RÉSEAUX WIFI DÉTECTÉS\n\n"
                    for line in lines:
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 2:
                                ssid = parts[1] if parts[1] != '--' else 'Réseau caché'
                                signal = parts[5] if len(parts) > 5 else 'N/A'
                                response += f"📡 {ssid} (Signal: {signal})\n"
                    
                    return response
                else:
                    return "❌ Impossible de scanner les réseaux WiFi"
                    
            elif system == "Darwin":  # macOS
                result = subprocess.run(
                    ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')[1:11]
                    
                    response = "📶 RÉSEAUX WIFI DÉTECTÉS\n\n"
                    for line in lines:
                        if line.strip():
                            parts = line.split()
                            if parts:
                                ssid = parts[0]
                                response += f"📡 {ssid}\n"
                    
                    return response
                else:
                    return "❌ Impossible de scanner les réseaux WiFi"
            else:
                return "⚠️ Scan WiFi disponible uniquement sur Linux/macOS"
                
        except Exception as e:
            return f"❌ Erreur scan WiFi: {e}"
    
    def show_help(self):
        """Affiche l'aide"""
        return """🌐 OUTILS RÉSEAU

📌 Commandes disponibles:
• ext NetworkTools ping [host] - Ping un hôte
• ext NetworkTools scan [ip] - Scanner les ports
• ext NetworkTools speed - Test de vitesse
• ext NetworkTools ip [adresse] - Info géolocalisation IP
• ext NetworkTools wifi - Scanner réseaux WiFi
• ext NetworkTools help - Cette aide

💡 Exemples:
• ext NetworkTools ping google.com
• ext NetworkTools scan 192.168.1.1
• ext NetworkTools speed
• ext NetworkTools ip 8.8.8.8
• ext NetworkTools wifi

🔧 Fonctionnalités:
• Ping avec statistiques détaillées
• Scan des ports communs
• Test de vitesse et latence
• Géolocalisation d'adresses IP
• Détection des réseaux WiFi"""
    
    def get_commands(self):
        return ["ping", "scan", "speed", "ip", "wifi", "help"]