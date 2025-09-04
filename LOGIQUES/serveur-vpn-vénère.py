class AdvancedVPNServer(AdvancedVPNCore):
    def __init__(self, host='0.0.0.0', port=1194):
        super().__init__()
        self.host = host
        self.port = port
        self.running = False
        self.ip_pool = self.generate_ip_pool()
        self.client_ips = {}
        
    def generate_ip_pool(self) -> List[str]:
        """Génère un pool d'IPs virtuelles"""
        pool = []
        for i in range(2, 254):
            for j in range(2, 254):
                pool.append(f"10.{i}.{j}.1")
        return pool
    
    def assign_virtual_ip(self, client_id: str) -> str:
        """Assigne une IP virtuelle aléatoire"""
        if client_id in self.client_ips:
            return self.client_ips[client_id]
        
        available_ips = [ip for ip in self.ip_pool if ip not in self.client_ips.values()]
        if available_ips:
            assigned_ip = random.choice(available_ips)
            self.client_ips[client_id] = assigned_ip
            return assigned_ip
        else:
            # Réutilise une IP ancienne
            oldest_client = min(self.client_ips.keys(), key=lambda k: self.clients[k].get('last_seen', 0))
            assigned_ip = self.client_ips[oldest_client]
            self.client_ips[client_id] = assigned_ip
            return assigned_ip
    
    def rotate_client_ips(self):
        """Rotation périodique des IPs clients"""
        current_time = time.time()
        if current_time - self.last_ip_rotation > self.ip_rotation_interval:
            print("Rotation des IPs clients...")
            for client_id in self.client_ips:
                new_ip = random.choice(self.ip_pool)
                self.client_ips[client_id] = new_ip
                # Notifie le client du changement d'IP
                if client_id in self.clients:
                    self.send_ip_update(client_id, new_ip)
            
            self.last_ip_rotation = current_time
    
    def send_ip_update(self, client_id: str, new_ip: str):
        """Envoie une mise à jour d'IP au client"""
        update_packet = {
            'type': 'ip_update',
            'new_ip': new_ip,
            'timestamp': time.time()
        }
        
        encrypted_update = self.encrypt_packet(json.dumps(update_packet).encode())
        self.send_to_client(client_id, encrypted_update)
    
    def handle_http_traffic(self, data: bytes) -> bytes:
        """Intercepte et modifie le trafic HTTP"""
        try:
            if data.startswith(b'GET') or data.startswith(b'POST') or data.startswith(b'HTTP'):
                headers_end = data.find(b'\r\n\r\n')
                if headers_end != -1:
                    headers_part = data[:headers_end + 4]
                    body = data[headers_end + 4:]
                    
                    # Parse les headers
                    headers = {}
                    lines = headers_part.split(b'\r\n')
                    for line in lines[1:]:  # Skip la première ligne (GET/POST)
                        if b':' in line:
                            key, value = line.split(b':', 1)
                            headers[key.strip().decode()] = value.strip().decode()
                    
                    # Obfuscation des headers
                    obfuscated_headers = self.obfuscate_headers(headers)
                    
                    # Reconstruit les headers
                    new_headers = [lines[0]]  # Ligne de requête
                    for key, value in obfuscated_headers.items():
                        new_headers.append(f"{key}: {value}".encode())
                    
                    new_headers_part = b'\r\n'.join(new_headers) + b'\r\n\r\n'
                    return new_headers_part + body
        except:
            pass
        
        return data
    
    def start_server(self):
        """Démarre le serveur VPN avec gestion multi-nœuds"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        
        self.running = True
        print(f"Serveur VPN avancé démarré sur {self.host}:{self.port}")
        
        # Thread de rotation IP
        rotation_thread = threading.Thread(target=self.ip_rotation_worker)
        rotation_thread.daemon = True
        rotation_thread.start()
        
        client_counter = 0
        
        while self.running:
            try:
                readable, _, _ = select.select([self.socket], [], [], 1.0)
                
                if readable:
                    client_sock, client_addr = self.socket.accept()
                    client_counter += 1
                    client_id = f"client_{client_counter}"
                    
                    thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_sock, client_addr, client_id)
                    )
                    thread.daemon = True
                    thread.start()
                
                # Rotation périodique des IPs
                self.rotate_client_ips()
                
            except KeyboardInterrupt:
                self.stop_server()
            except Exception as e:
                print(f"Erreur serveur: {e}")
    
    def ip_rotation_worker(self):
        """Worker pour la rotation automatique des IPs"""
        while self.running:
            time.sleep(self.ip_rotation_interval)
            self.rotate_client_ips()