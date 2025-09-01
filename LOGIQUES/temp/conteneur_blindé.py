import hashlib
import pickle
import base64
import zlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

class ConteneurBlinde:
    def __init__(self, code_acces: str, taille_paquet: int = 1024):
        self.code_acces = hashlib.sha256(code_acces.encode()).digest()
        self.taille_paquet = taille_paquet
        self.paquets = []
        self.est_verrouille = True
        self.contenu_original = None
    
    def _chiffrer(self, data: bytes) -> bytes:
        cipher = AES.new(self.code_acces, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        return cipher.iv + ct_bytes
    
    def _dechiffrer(self, data: bytes) -> bytes:
        iv = data[:16]
        ct = data[16:]
        cipher = AES.new(self.code_acces, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt
    
    def charger_contenu(self, contenu: any, code: str) -> bool:
        if hashlib.sha256(code.encode()).digest() != self.code_acces:
            return False
        
        # Sérialisation et compression
        data_serialise = pickle.dumps(contenu)
        data_compresse = zlib.compress(data_serialise)
        data_chiffre = self._chiffrer(data_compresse)
        
        # Morcellement en paquets
        self.paquets = []
        for i in range(0, len(data_chiffre), self.taille_paquet):
            paquet = data_chiffre[i:i + self.taille_paquet]
            paquet_hash = hashlib.sha256(paquet).hexdigest()
            self.paquets.append({
                'index': i // self.taille_paquet,
                'data': base64.b64encode(paquet).decode(),
                'hash': paquet_hash
            })
        
        self.est_verrouille = True
        return True
    
    def obtenir_paquets(self) -> list:
        return self.paquets if self.est_verrouille else []
    
    def reconstruire_contenu(self, code: str, paquets_recus: list) -> any:
        if hashlib.sha256(code.encode()).digest() != self.code_acces:
            return None
        
        # Vérification intégrité des paquets
        paquets_tries = sorted(paquets_recus, key=lambda x: x['index'])
        data_chiffre = b''
        
        for paquet in paquets_tries:
            data_paquet = base64.b64decode(paquet['data'])
            if hashlib.sha256(data_paquet).hexdigest() != paquet['hash']:
                raise ValueError("Intégrité du paquet compromise")
            data_chiffre += data_paquet
        
        # Déchiffrement et reconstruction
        try:
            data_dechiffre = self._dechiffrer(data_chiffre)
            data_decompresse = zlib.decompress(data_dechiffre)
            contenu = pickle.loads(data_decompresse)
            
            self.est_verrouille = False
            self.contenu_original = contenu
            return contenu
            
        except Exception as e:
            raise ValueError(f"Erreur de reconstruction: {e}")
    
    def est_accessible(self) -> bool:
        return not self.est_verrouille
    
    def verrouiller(self):
        self.est_verrouille = True
        self.contenu_original = None