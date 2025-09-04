import threading
import time
import random

class VpnManager:
    """
    Gère l'état et la simulation d'une connexion VPN "Vénère".
    Cette classe est conçue pour être utilisée par l'API principale.
    """
    def __init__(self):
        self.is_connected = False
        self.status_message = "Déconnecté"
        self.virtual_ip = None
        self.node_chain = []
        self.connection_thread = None
        # L'adresse du proxy sera maintenant gérée par la configuration globale.
        # On la reçoit en paramètre au moment de la connexion.
        self.proxy_address = None

    def get_status(self):
        """Retourne l'état actuel du VPN."""
        return {
            "status": "success",
            "is_connected": self.is_connected,
            "message": self.status_message,
            "virtual_ip": self.virtual_ip,
            "node_chain": self.node_chain,
            "proxy_address": self.proxy_address if self.is_connected else None
        }

    def _connection_task(self, window):
        """Tâche de connexion simulée s'exécutant dans un thread."""
        try:
            # 1. Simuler la construction de la chaîne de nœuds
            self.status_message = "Construction de la chaîne de relais..."
            window.events.vpn_status_update.fire(self.get_status())
            time.sleep(random.uniform(1, 3))
            
            num_hops = random.randint(2, 4)
            self.node_chain = [f"Relais {i+1} ({random.randint(1,255)}.{random.randint(1,255)}...)" for i in range(num_hops)]
            self.node_chain.append("Serveur Final")
            
            # 2. Simuler la connexion à travers la chaîne
            self.status_message = f"Connexion via {len(self.node_chain)} sauts..."
            window.events.vpn_status_update.fire(self.get_status())
            time.sleep(random.uniform(2, 4))

            # 3. Connexion établie
            self.is_connected = True
            self.virtual_ip = f"10.{random.randint(2,254)}.{random.randint(2,254)}.1"
            self.status_message = f"Connecté. IP Virtuelle : {self.virtual_ip}"
            window.events.vpn_status_update.fire(self.get_status())

            # 4. Simuler la rotation d'IP en arrière-plan
            while self.is_connected:
                time.sleep(random.uniform(20, 40)) # Intervalle de rotation simulé
                if self.is_connected:
                    self.virtual_ip = f"10.{random.randint(2,254)}.{random.randint(2,254)}.1"
                    self.status_message = f"IP Rotée. Nouvelle IP : {self.virtual_ip}"
                    window.events.vpn_status_update.fire(self.get_status())

        except Exception as e:
            self.is_connected = False
            self.status_message = f"Erreur de connexion : {e}"
            window.events.vpn_status_update.fire(self.get_status())

    def start(self, proxy_address, window):
        """Démarre la connexion VPN dans un thread séparé."""
        if not self.is_connected:
            self.proxy_address = proxy_address
            self.connection_thread = threading.Thread(target=self._connection_task, args=(window,))
            self.connection_thread.daemon = True
            self.connection_thread.start()

    def stop(self, window):
        """Arrête la connexion VPN."""
        if self.is_connected:
            self.is_connected = False
            self.status_message = "Déconnexion en cours..."
            window.events.vpn_status_update.fire(self.get_status())
            time.sleep(1) # Simule le délai de déconnexion
            self.status_message = "Déconnecté"
            self.virtual_ip = None
            self.node_chain = []
            self.proxy_address = None
            self.connection_thread = None # Le thread va se terminer car is_connected est False
        
        window.events.vpn_status_update.fire(self.get_status())