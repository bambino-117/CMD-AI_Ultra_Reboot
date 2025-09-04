class AdvancedVPNClient(AdvancedVPNCore):
    def __init__(self, server_host, server_port):
        super().__init__()
        self.server_host = server_host
        self.server_port = server_port
        self.connected = False
        self.virtual_ip = None
        self.node_chain = []
        
    def build_node_chain(self, target_server: str) -> List[Dict]:
        """Construit une chaîne de nœuds pour le routing"""
        chain = []
        available_nodes = [n for n in self.nodes if n['active']]
        
        if not available_nodes:
            return chain
        
        # Sélectionne 2-4 nœuds aléatoires
        num_hops = random.randint(2, min(4, len(available_nodes)))
        for _ in range(num_hops):
            node = random.choice(available_nodes)
            chain.append(node)
            available_nodes.remove(node)
        
        # Ajoute le serveur final
        chain.append({'host': target_server, 'port': self.server_port, 'type': 'final'})
        return chain
    
    def connect_through_chain(self, node_chain: List[Dict]):
        """Se connecte à travers une chaîne de nœuds"""
        current_socket = None
        
        try:
            for i, node in enumerate(node_chain):
                is_final = (i == len(node_chain) - 1)
                
                if current_socket:
                    # Forward la connexion existante
                    self.forward_through_node(current_socket, node, is_final)
                else:
                    # Première connexion
                    current_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    current_socket.connect((node['host'], node['port']))
                    
                    if is_final:
                        self.connected = True
                        print(f"Connecté via {len(node_chain)} nœuds")
                        return current_socket
                        
        except Exception as e:
            print(f"Erreur connexion multi-sauts: {e}")
            if current_socket:
                current_socket.close()
            return None
    
    def forward_through_node(self, existing_socket, next_node, is_final: bool):
        """Forward une connexion à travers un nœud"""
        # Implémentation du forwarding à travers les nœuds
        pass
    
    def handle_ip_update(self, packet: bytes):
        """Traite les mises à jour d'IP du serveur"""
        try:
            decrypted = self.decrypt_packet(packet)
            update_data = json.loads(decrypted.decode())
            
            if update_data['type'] == 'ip_update':
                old_ip = self.virtual_ip
                self.virtual_ip = update_data['new_ip']
                print(f"IP virtuelle mise à jour: {old_ip} -> {self.virtual_ip}")
                
        except:
            pass
    
    def start_ip_rotation(self):
        """Démarre la rotation automatique d'IP côté client"""
        while self.connected:
            time.sleep(self.ip_rotation_interval + random.randint(-60, 60))
            if self.connected:
                # Demande une nouvelle IP au serveur
                self.request_new_ip()
    
    def request_new_ip(self):
        """Demande une nouvelle IP virtuelle au serveur"""
        request = {
            'type': 'ip_request',
            'timestamp': time.time()
        }
        
        encrypted_request = self.encrypt_packet(json.dumps(request).encode())
        self.send_packet(encrypted_request)