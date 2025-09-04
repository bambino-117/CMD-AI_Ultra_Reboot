import socket
import threading
import select
import struct
import hashlib
import os
import time
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac
import json
from typing import List, Dict, Optional
import base64

class AdvancedVPNCore:
    def __init__(self, tunnel_ip='10.8.0.1', subnet_mask='255.255.255.0'):
        self.tunnel_ip = tunnel_ip
        self.subnet_mask = subnet_mask
        self.clients = {}
        self.nodes = []  # Liste des nœuds intermédiaires
        self.current_node_index = 0
        self.ip_rotation_interval = 300  # Rotation IP toutes les 5 minutes
        self.last_ip_rotation = time.time()
        
        # Clés de chiffrement
        self.encryption_key = self.generate_key(32)  # AES-256
        self.hmac_key = self.generate_key(32)
        
    def generate_key(self, length: int) -> bytes:
        """Génère une clé de chiffrement"""
        return os.urandom(length)
    
    def rotate_ip(self):
        """Génère une nouvelle IP virtuelle pour le tunnel"""
        new_ip = f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        self.tunnel_ip = new_ip
        return new_ip
    
    def add_node(self, node_host: str, node_port: int, node_type: str = "relay"):
        """Ajoute un nœud intermédiaire"""
        node = {
            'host': node_host,
            'port': node_port,
            'type': node_type,
            'latency': 0,
            'active': True
        }
        self.nodes.append(node)
    
    def get_next_node(self) -> Optional[Dict]:
        """Sélectionne le prochain nœud (round-robin avec vérification)"""
        if not self.nodes:
            return None
        
        start_index = self.current_node_index
        attempts = 0
        
        while attempts < len(self.nodes):
            node = self.nodes[self.current_node_index]
            self.current_node_index = (self.current_node_index + 1) % len(self.nodes)
            
            if node['active']:
                return node
            
            attempts += 1
        
        return None
    
    def obfuscate_headers(self, headers: Dict) -> Dict:
        """Brouille les en-têtes HTTP sensibles"""
        obfuscated = headers.copy()
        
        # X-Forwarded-For obfuscation
        if 'X-Forwarded-For' in obfuscated:
            real_ips = obfuscated['X-Forwarded-For'].split(',')
            # Ajoute des IPs factices et mélange
            fake_ips = [f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}" 
                       for _ in range(random.randint(1, 3))]
            all_ips = real_ips + fake_ips
            random.shuffle(all_ips)
            obfuscated['X-Forwarded-For'] = ', '.join(all_ips)
        
        # Headers communs à brouiller
        headers_to_obfuscate = [
            'X-Real-IP', 'X-Client-IP', 'Forwarded',
            'CF-Connecting-IP', 'True-Client-IP'
        ]
        
        for header in headers_to_obfuscate:
            if header in obfuscated:
                obfuscated[header] = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        # Ajoute des headers factices
        fake_headers = {
            'X-Proxy-ID': base64.b64encode(os.urandom(8)).decode(),
            'Via': f"1.1 {random.choice(['squid', 'nginx', 'apache'])}",
            'X-Request-ID': hashlib.md5(os.urandom(16)).hexdigest()
        }
        
        obfuscated.update(fake_headers)
        return obfuscated
    
    def encrypt_packet(self, data: bytes, additional_data: bytes = b"") -> bytes:
        """Chiffre un paquet avec AES-GCM et authentification"""
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        
        # Authenticate additional data if provided
        if additional_data:
            encryptor.authenticate_additional_data(additional_data)
        
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        return iv + encryptor.tag + encrypted_data
    
    def decrypt_packet(self, encrypted_data: bytes, additional_data: bytes = b"") -> bytes:
        """Déchiffre un paquet avec vérification d'authenticité"""
        iv = encrypted_data[:12]
        tag = encrypted_data[12:28]
        data = encrypted_data[28:]
        
        cipher = Cipher(algorithms.AES(self.encryption_key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        
        if additional_data:
            decryptor.authenticate_additional_data(additional_data)
        
        return decryptor.update(data) + decryptor.finalize()
    
    def create_multi_hop_header(self, packet_type: str, final_dest: str, hops: int = 3) -> bytes:
        """Crée un en-tête multi-sauts"""
        timestamp = int(time.time())
        hop_list = [self.generate_hop_info() for _ in range(hops)]
        
        header_data = {
            'type': packet_type,
            'final_destination': final_dest,
            'timestamp': timestamp,
            'hops': hop_list,
            'current_hop': 0,
            'ttl': hops
        }
        
        return json.dumps(header_data).encode()
    
    def generate_hop_info(self) -> Dict:
        """Génère des informations pour un saut"""
        return {
            'node_id': hashlib.md5(os.urandom(16)).hexdigest()[:8],
            'encryption_layer': random.choice(['aes-gcm', 'chacha20']),
            'timestamp_delta': random.randint(-100, 100)
        }
    
    def process_multi_hop(self, packet: bytes) -> bytes:
        """Traite un paquet multi-sauts"""
        try:
            header = packet[:256]  Premier 256 bytes pour l'en-tête
            payload = packet[256:]
            
            header_data = json.loads(header.decode())
            
            if header_data['current_hop'] >= header_data['ttl']:
                return payload  # Dernier saut, retourne le payload
            
            # Incrémente le hop count et forwarde
            header_data['current_hop'] += 1
            next_header = json.dumps(header_data).encode()
            
            return next_header + payload
            
        except:
            return packet  # En cas d'erreur, forwarde tel quel