from core.base_extension import BaseExtension
import psutil
import platform
import json
from datetime import datetime

class SystemMonitorExtension(BaseExtension):
    def __init__(self):
        super().__init__()
        self.name = "SystemMonitor"
        self.version = "1.1.0"
        self.description = "Monitoring système: CPU, RAM, disque, processus, température"
        self.author = "CMD-AI Team"
    
    def initialize(self, app_context):
        self.app_context = app_context
    
    def execute(self, command, args=None):
        if command == "status":
            return self.get_system_status()
        elif command == "processes":
            return self.get_top_processes()
        elif command == "disk":
            return self.get_disk_usage()
        elif command == "network":
            return self.get_network_stats()
        elif command == "temp":
            return self.get_temperatures()
        elif command == "monitor":
            return self.start_monitoring()
        elif command == "help":
            return self.show_help()
        else:
            return "Commandes: status, processes, disk, network, temp, monitor, help"
    
    def get_system_status(self):
        """Statut général du système"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Mémoire
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Système
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            result = f"🖥️ STATUT SYSTÈME\n\n"
            result += f"💻 OS: {platform.system()} {platform.release()}\n"
            result += f"⏰ Démarré: {boot_time.strftime('%d/%m/%Y %H:%M')}\n"
            result += f"🕐 Uptime: {str(uptime).split('.')[0]}\n\n"
            
            result += f"🧠 CPU ({cpu_count} cœurs):\n"
            result += f"   Utilisation: {cpu_percent}%\n"
            if cpu_freq:
                result += f"   Fréquence: {cpu_freq.current:.0f} MHz\n"
            
            result += f"\n💾 MÉMOIRE:\n"
            result += f"   RAM: {self._format_bytes(memory.used)} / {self._format_bytes(memory.total)} ({memory.percent}%)\n"
            result += f"   Swap: {self._format_bytes(swap.used)} / {self._format_bytes(swap.total)} ({swap.percent}%)\n"
            
            # Indicateur de performance
            if cpu_percent > 80 or memory.percent > 80:
                result += f"\n⚠️ Système sous charge élevée"
            elif cpu_percent < 20 and memory.percent < 50:
                result += f"\n✅ Système performant"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur statut système: {e}"
    
    def get_top_processes(self):
        """Top des processus consommateurs"""
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Trier par CPU puis par mémoire
            processes.sort(key=lambda x: (x['cpu_percent'] or 0, x['memory_percent'] or 0), reverse=True)
            
            result = f"📊 TOP PROCESSUS (CPU/RAM)\n\n"
            result += f"{'PID':<8} {'PROCESSUS':<20} {'CPU%':<8} {'RAM%':<8}\n"
            result += "-" * 50 + "\n"
            
            for proc in processes[:15]:
                pid = proc['pid']
                name = (proc['name'] or 'N/A')[:18]
                cpu = f"{proc['cpu_percent'] or 0:.1f}%"
                mem = f"{proc['memory_percent'] or 0:.1f}%"
                
                result += f"{pid:<8} {name:<20} {cpu:<8} {mem:<8}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur processus: {e}"
    
    def get_disk_usage(self):
        """Usage des disques"""
        try:
            result = f"💽 USAGE DISQUES\n\n"
            
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    result += f"📁 {partition.device}\n"
                    result += f"   Point de montage: {partition.mountpoint}\n"
                    result += f"   Système: {partition.fstype}\n"
                    result += f"   Total: {self._format_bytes(usage.total)}\n"
                    result += f"   Utilisé: {self._format_bytes(usage.used)} ({usage.percent}%)\n"
                    result += f"   Libre: {self._format_bytes(usage.free)}\n"
                    
                    # Barre de progression
                    bar_length = 20
                    filled = int(bar_length * usage.percent / 100)
                    bar = "█" * filled + "░" * (bar_length - filled)
                    result += f"   [{bar}] {usage.percent}%\n\n"
                    
                except PermissionError:
                    result += f"📁 {partition.device} - Accès refusé\n\n"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur disques: {e}"
    
    def get_network_stats(self):
        """Statistiques réseau"""
        try:
            net_io = psutil.net_io_counters()
            net_if = psutil.net_if_addrs()
            
            result = f"🌐 STATISTIQUES RÉSEAU\n\n"
            
            # Statistiques globales
            result += f"📊 Trafic global:\n"
            result += f"   ⬇️ Reçu: {self._format_bytes(net_io.bytes_recv)}\n"
            result += f"   ⬆️ Envoyé: {self._format_bytes(net_io.bytes_sent)}\n"
            result += f"   📦 Paquets reçus: {net_io.packets_recv:,}\n"
            result += f"   📦 Paquets envoyés: {net_io.packets_sent:,}\n\n"
            
            # Interfaces réseau
            result += f"🔌 Interfaces réseau:\n"
            for interface, addresses in net_if.items():
                result += f"   • {interface}:\n"
                for addr in addresses:
                    if addr.family == 2:  # IPv4
                        result += f"     IPv4: {addr.address}\n"
                    elif addr.family == 17:  # MAC
                        result += f"     MAC: {addr.address}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur réseau: {e}"
    
    def get_temperatures(self):
        """Températures du système"""
        try:
            temps = psutil.sensors_temperatures()
            
            if not temps:
                return "🌡️ Capteurs de température non disponibles sur ce système"
            
            result = f"🌡️ TEMPÉRATURES SYSTÈME\n\n"
            
            for name, entries in temps.items():
                result += f"🔥 {name}:\n"
                for entry in entries:
                    temp = entry.current
                    label = entry.label or "Capteur"
                    
                    # Indicateur de température
                    if temp > 80:
                        status = "🔴 CHAUD"
                    elif temp > 60:
                        status = "🟡 TIÈDE"
                    else:
                        status = "🟢 OK"
                    
                    result += f"   {label}: {temp}°C {status}\n"
                result += "\n"
            
            return result
            
        except Exception as e:
            return "🌡️ Capteurs de température non supportés sur ce système"
    
    def start_monitoring(self):
        """Monitoring en temps réel (simulation)"""
        try:
            # Snapshot actuel
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            result = f"📈 MONITORING TEMPS RÉEL\n\n"
            result += f"🕐 {datetime.now().strftime('%H:%M:%S')}\n\n"
            
            # CPU avec barre
            cpu_bar = self._create_progress_bar(cpu, 100)
            result += f"🧠 CPU: [{cpu_bar}] {cpu}%\n"
            
            # RAM avec barre
            ram_bar = self._create_progress_bar(memory.percent, 100)
            result += f"💾 RAM: [{ram_bar}] {memory.percent}%\n"
            
            # Top 3 processus
            processes = []
            for proc in psutil.process_iter(['name', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except:
                    continue
            
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            result += f"\n🔝 Top processus:\n"
            for proc in processes[:3]:
                name = (proc['name'] or 'N/A')[:15]
                cpu_proc = proc['cpu_percent'] or 0
                result += f"   • {name}: {cpu_proc}%\n"
            
            result += f"\n💡 Utilisez 'ext SystemMonitor status' pour plus de détails"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur monitoring: {e}"
    
    def _format_bytes(self, bytes_value):
        """Formate les octets en unités lisibles"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024
        return f"{bytes_value:.1f} PB"
    
    def _create_progress_bar(self, value, max_value, length=15):
        """Crée une barre de progression"""
        filled = int(length * value / max_value)
        return "█" * filled + "░" * (length - filled)
    
    def show_help(self):
        """Affiche l'aide"""
        return """🖥️ MONITORING SYSTÈME

📌 Commandes disponibles:
• ext SystemMonitor status - Statut général système
• ext SystemMonitor processes - Top processus
• ext SystemMonitor disk - Usage des disques
• ext SystemMonitor network - Statistiques réseau
• ext SystemMonitor temp - Températures système
• ext SystemMonitor monitor - Monitoring temps réel
• ext SystemMonitor help - Cette aide

💡 Exemples:
• ext SystemMonitor status
• ext SystemMonitor processes
• ext SystemMonitor disk
• ext SystemMonitor monitor

🔧 Fonctionnalités:
• Monitoring CPU, RAM, disques
• Top des processus consommateurs
• Statistiques réseau détaillées
• Températures système (si supporté)
• Monitoring temps réel"""
    
    def get_commands(self):
        return ["status", "processes", "disk", "network", "temp", "monitor", "help"]