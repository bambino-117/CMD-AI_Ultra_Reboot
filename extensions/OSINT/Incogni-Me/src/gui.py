import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    email: str
    token: str

class IncogniMeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Incogni-Me - Gestionnaire d'Empreinte Numérique")
        self.root.geometry("800x600")
        
        self.current_user: Optional[User] = None
        self.api_base_url = "http://localhost:8001"
        
        self.setup_gui()

    def setup_gui(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Zone de connexion
        self.login_frame = ttk.LabelFrame(self.main_frame, text="Connexion", padding="5")
        self.login_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.login_frame, text="Email:").grid(row=0, column=0, padx=5)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(self.login_frame, textvariable=self.email_var)
        self.email_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.login_frame, text="Mot de passe:").grid(row=0, column=2, padx=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.login_frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=0, column=3, padx=5)

        self.login_button = ttk.Button(self.login_frame, text="Connexion", command=self.login)
        self.login_button.grid(row=0, column=4, padx=5)
        
        self.register_button = ttk.Button(self.login_frame, text="S'inscrire", command=self.register)
        self.register_button.grid(row=0, column=5, padx=5)

        # Zone de gestion des identités
        self.identity_frame = ttk.LabelFrame(self.main_frame, text="Gestion des identités", padding="5")
        self.identity_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.identity_var = tk.StringVar()
        self.identity_entry = ttk.Entry(self.identity_frame, textvariable=self.identity_var, width=40)
        self.identity_entry.grid(row=0, column=0, padx=5)

        self.add_identity_button = ttk.Button(self.identity_frame, text="Ajouter une identité", command=self.add_identity)
        self.add_identity_button.grid(row=0, column=1, padx=5)

        self.scan_button = ttk.Button(self.identity_frame, text="Lancer un scan", command=self.start_scan)
        self.scan_button.grid(row=0, column=2, padx=5)

        # Liste des résultats
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Résultats", padding="5")
        self.results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.results_tree = ttk.Treeview(self.results_frame, columns=("type", "platform", "url", "status"), 
                                       show="headings", height=10)
        
        self.results_tree.heading("type", text="Type")
        self.results_tree.heading("platform", text="Plateforme")
        self.results_tree.heading("url", text="URL")
        self.results_tree.heading("status", text="Statut")

        self.results_tree.column("type", width=100)
        self.results_tree.column("platform", width=100)
        self.results_tree.column("url", width=300)
        self.results_tree.column("status", width=100)

        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Actions pour les résultats
        self.action_frame = ttk.Frame(self.results_frame)
        self.action_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.request_deletion_button = ttk.Button(self.action_frame, text="Demander la suppression", 
                                                command=self.request_deletion)
        self.request_deletion_button.pack(side=tk.LEFT, padx=5)

        # Désactiver les contrôles jusqu'à la connexion
        self.update_ui_state(False)

    def update_ui_state(self, is_logged_in: bool):
        state = "normal" if is_logged_in else "disabled"
        self.identity_entry.configure(state=state)
        self.add_identity_button.configure(state=state)
        self.scan_button.configure(state=state)
        self.request_deletion_button.configure(state=state)

    def login(self):
        try:
            response = requests.post(
                f"{self.api_base_url}/token",
                data={
                    "username": self.email_var.get(),
                    "password": self.password_var.get()
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.current_user = User(
                    id=data["user_id"],
                    email=self.email_var.get(),
                    token=data["access_token"]
                )
                messagebox.showinfo("Succès", "Connexion réussie!")
                self.update_ui_state(True)
                self.load_footprint_items()
            else:
                messagebox.showerror("Erreur", "Échec de la connexion")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de connexion: {str(e)}")

    def register(self):
        try:
            response = requests.post(
                f"{self.api_base_url}/users",
                json={
                    "email": self.email_var.get(),
                    "password": self.password_var.get()
                }
            )
            if response.status_code == 200:
                messagebox.showinfo("Succès", "Inscription réussie! Vous pouvez maintenant vous connecter.")
            else:
                messagebox.showerror("Erreur", "Échec de l'inscription")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'inscription: {str(e)}")

    def add_identity(self):
        if not self.current_user:
            return
        
        try:
            headers = {"Authorization": f"Bearer {self.current_user.token}"}
            response = requests.post(
                f"{self.api_base_url}/users/me/identities",
                headers=headers,
                json={"identity": self.identity_var.get()}
            )
            if response.status_code == 200:
                messagebox.showinfo("Succès", "Identité ajoutée avec succès!")
                self.identity_var.set("")  # Clear the entry
            else:
                messagebox.showerror("Erreur", "Impossible d'ajouter l'identité")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'identité: {str(e)}")

    def start_scan(self):
        if not self.current_user:
            return
        
        try:
            headers = {"Authorization": f"Bearer {self.current_user.token}"}
            response = requests.post(
                f"{self.api_base_url}/footprint/scan",
                headers=headers
            )
            if response.status_code == 200:
                self.load_footprint_items()
                messagebox.showinfo("Succès", "Scan terminé!")
            else:
                messagebox.showerror("Erreur", "Impossible de lancer le scan")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du scan: {str(e)}")

    def load_footprint_items(self):
        if not self.current_user:
            return
        
        try:
            headers = {"Authorization": f"Bearer {self.current_user.token}"}
            response = requests.get(
                f"{self.api_base_url}/footprint/items",
                headers=headers
            )
            if response.status_code == 200:
                items = response.json()
                # Clear existing items
                for item in self.results_tree.get_children():
                    self.results_tree.delete(item)
                # Add new items
                for item in items:
                    self.results_tree.insert("", tk.END, values=(
                        item["type"],
                        item["platform"],
                        item["url"],
                        item["status"]
                    ))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des résultats: {str(e)}")

    def request_deletion(self):
        if not self.current_user:
            return
        
        selected = self.results_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un élément à supprimer")
            return
        
        item = self.results_tree.item(selected[0])
        try:
            headers = {"Authorization": f"Bearer {self.current_user.token}"}
            response = requests.post(
                f"{self.api_base_url}/footprint/items/{item['id']}/requests",
                headers=headers,
                json={"request_type": "REMOVAL"}
            )
            if response.status_code == 200:
                messagebox.showinfo("Succès", "Demande de suppression envoyée!")
                self.load_footprint_items()
            else:
                messagebox.showerror("Erreur", "Impossible d'envoyer la demande de suppression")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la demande de suppression: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = IncogniMeGUI()
    app.run()
