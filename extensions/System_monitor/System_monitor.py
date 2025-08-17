import psutil
import platform
import socket
from datetime import datetime

class SystemMonitorExtension:
    def initialize(self, _):
        pass

    def _get_temp_status(self, temp):
        if temp is None:
            return ""
        if temp > 80:
            return "🔴 CHAUD"
        elif temp > 60:
            return "🟡 TIÈDE"
        else:
            return "🟢 OK"

    def _format_bytes(self, bytes_value):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"

    def get_system_info(self):
        uname = platform.uname()
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        return {
            'system': uname.system,
            'node_name': uname.node,
            'release': uname.release,
            'version': uname.version,
            'machine': uname.machine,
            'processor': uname.processor,
            'boot_time': boot_time.strftime("%Y-%m-%d %H:%M:%S"),
            'uptime': str(datetime.now() - boot_time).split('.')[0]
        }

    def get_cpu_info(self):
        cpu_freq = psutil.cpu_freq()
        return {
            'physical_cores': psutil.cpu_count(logical=False),
            'total_cores': psutil.cpu_count(logical=True),
            'max_frequency': f"{cpu_freq.max:.2f}Mhz" if cpu_freq else "N/A",
            'min_frequency': f"{cpu_freq.min:.2f}Mhz" if cpu_freq else "N/A",
            'current_frequency': f"{cpu_freq.current:.2f}Mhz" if cpu_freq else "N/A",
            'cpu_usage_per_core': [f"{x:.1f}%" for x in psutil.cpu_percent(percpu=True, interval=1)]
        }

    def get_memory_info(self):
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            'total': self._format_bytes(svmem.total),
            'available': self._format_bytes(svmem.available),
            'used': self._format_bytes(svmem.used),
            'percentage': svmem.percent,
            'swap_total': self._format_bytes(swap.total),
            'swap_used': self._format_bytes(swap.used),
            'swap_free': self._format_bytes(swap.free),
            'swap_percentage': swap.percent
        }

    def get_disk_info(self):
        partitions = psutil.disk_partitions()
        disk_info = []
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'file_system': partition.fstype,
                    'total_size': self._format_bytes(partition_usage.total),
                    'used': self._format_bytes(partition_usage.used),
                    'free': self._format_bytes(partition_usage.free),
                    'percentage': round((partition_usage.used / partition_usage.total) * 100, 1)
                })
            except PermissionError:
                continue
        return disk_info

    def get_network_info(self):
        net_io = psutil.net_io_counters()
        interfaces = []
        for interface_name, interface_addresses in psutil.net_if_addrs().items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    interfaces.append({
                        'interface': interface_name,
                        'ip': address.address,
                        'netmask': address.netmask,
                        'broadcast': address.broadcast
                    })
        return {
            'total_bytes_sent': self._format_bytes(net_io.bytes_sent),
            'total_bytes_received': self._format_bytes(net_io.bytes_recv),
            'interfaces': interfaces
        }

    def get_temperatures_data(self):
        temps = {}
        try:
            temps_psutil = psutil.sensors_temperatures()
            if temps_psutil:
                for name, entries in temps_psutil.items():
                    for entry in entries:
                        if "cpu" in name.lower() or "core" in name.lower():
                            temps.setdefault('cpu', []).append({
                                'label': entry.label or 'Capteur',
                                'current': entry.current,
                                'status': self._get_temp_status(entry.current)
                            })
        except AttributeError:
            pass
        
        if not temps.get('cpu'):
            temps['cpu'] = [{'label': 'N/A', 'current': None, 'status': 'Non disponible'}]
        
        temps.setdefault('gpu', [{'label': 'N/A', 'current': None, 'status': 'Non disponible'}])
        temps.setdefault('ssd', [{'label': 'N/A', 'current': None, 'status': 'Non disponible'}])
        return temps

    def get_top_processes_data(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status', 'create_time']):
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status', 'create_time'])
                pinfo['memory_percent'] = round(pinfo['memory_percent'], 2)
                pinfo['create_time'] = datetime.fromtimestamp(pinfo['create_time']).strftime("%H:%M:%S")
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:15]

    def get_services_info(self):
        services = []
        try:
            for service in psutil.win_service_iter():
                try:
                    service_info = service.as_dict()
                    if service_info['status'] in ['running', 'stopped']:
                        services.append({
                            'name': service_info['name'],
                            'display_name': service_info['display_name'][:50] + '...' if len(service_info['display_name']) > 50 else service_info['display_name'],
                            'status': service_info['status']
                        })
                except Exception:
                    continue
        except AttributeError:
            services = [{'name': 'N/A', 'display_name': 'Services non disponibles sur ce système', 'status': 'N/A'}]
        return sorted(services, key=lambda s: s['status'], reverse=True)[:20]

    def get_battery_info(self):
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percent': battery.percent,
                    'power_plugged': battery.power_plugged,
                    'time_left': str(battery.secsleft // 3600) + 'h ' + str((battery.secsleft % 3600) // 60) + 'm' if battery.secsleft != psutil.POWER_TIME_UNLIMITED else 'Illimité'
                }
        except Exception:
            pass
        return None