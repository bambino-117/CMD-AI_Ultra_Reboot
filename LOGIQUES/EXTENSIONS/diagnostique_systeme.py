from .base_extension import BaseExtension
import docker
import docker.errors

class DiagnostiqueSysteme(BaseExtension):
    """
    Extension pour surveiller l'état et les ressources de la sandbox active
    (le conteneur Docker lancé par le Chargeur Universel).
    """
    NAME = "Diagnostic Système"
    DESCRIPTION = "Surveille les ressources (CPU, RAM, Réseau) de la sandbox en temps réel."
    SANDBOX_CONTAINER_NAME = "megastructure-sandbox"

    def __init__(self):
        """Initialise l'extension et le client Docker."""
        self.docker_client = None
        self.docker_available = False
        self.error_message = ""
        try:
            self.docker_client = docker.from_env(timeout=5)
            self.docker_client.ping()
            self.docker_available = True
        except Exception as e:
            self.error_message = f"Erreur de connexion à Docker: {e}"
            print(f"[Diagnostic Système] ERREUR: {self.error_message}")

    def execute(self, *args, **kwargs):
        """Méthode principale, alias pour get_sandbox_diagnostics."""
        return self.get_sandbox_diagnostics()

    def get_sandbox_diagnostics(self):
        """Récupère et formate les statistiques du conteneur de la sandbox."""
        if not self.docker_available:
            return {'status': 'error', 'message': self.error_message}

        try:
            container = self.docker_client.containers.get(self.SANDBOX_CONTAINER_NAME)
            if container.status != 'running':
                return {'status': 'stopped', 'message': 'La sandbox n\'est pas en cours d\'exécution.'}

            # Récupère les stats en une seule fois (pas en streaming)
            stats = container.stats(stream=False)

            # --- Analyse des statistiques ---
            # Mémoire
            mem_usage = stats.get('memory_stats', {}).get('usage', 0)
            mem_limit = stats.get('memory_stats', {}).get('limit', 1)
            mem_percent = (mem_usage / mem_limit) * 100 if mem_limit > 0 else 0

            # CPU
            cpu_percent = 0.0
            cpu_stats = stats.get('cpu_stats', {})
            precpu_stats = stats.get('precpu_stats', {})
            
            cpu_delta = cpu_stats.get('cpu_usage', {}).get('total_usage', 0) - precpu_stats.get('cpu_usage', {}).get('total_usage', 0)
            system_cpu_delta = cpu_stats.get('system_cpu_usage', 0) - precpu_stats.get('system_cpu_usage', 0)
            number_cpus = cpu_stats.get('online_cpus', 1)

            if system_cpu_delta > 0 and cpu_delta > 0:
                cpu_percent = (cpu_delta / system_cpu_delta) * number_cpus * 100.0

            # Réseau (simple lecture des octets)
            net_rx = 0
            net_tx = 0
            networks = stats.get('networks', {})
            if networks:
                # Prend la première interface réseau trouvée (généralement eth0)
                first_interface = next(iter(networks.values()), {})
                net_rx = first_interface.get('rx_bytes', 0)
                net_tx = first_interface.get('tx_bytes', 0)

            return {
                'status': 'running',
                'data': {
                    'cpu_usage': round(cpu_percent, 2),
                    'memory_usage': round(mem_usage / (1024 * 1024), 2), # en Mo
                    'memory_limit': round(mem_limit / (1024 * 1024), 2), # en Mo
                    'memory_percent': round(mem_percent, 2),
                    'network_rx_mb': round(net_rx / (1024 * 1024), 2),
                    'network_tx_mb': round(net_tx / (1024 * 1024), 2),
                    'container_id': container.short_id,
                    'container_status': container.status
                }
            }

        except docker.errors.NotFound:
            return {'status': 'stopped', 'message': 'La sandbox n\'est pas en cours d\'exécution.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur lors de la récupération des stats: {e}'}