from LOGIQUES.EXTENSIONS.base_extension import BaseExtension
import docker
import docker.errors
import threading
import os
import shutil

class UniversalLoaderExtension(BaseExtension):
    """
    Extension pour charger et exécuter des applications de différentes plateformes
    dans un environnement virtualisé (sandbox).
    """
    NAME = "Chargeur d'Applications Universel"
    DESCRIPTION = "Permet d'exécuter des applications de différents systèmes d'exploitation dans une sandbox."
    SANDBOX_CONTAINER_NAME = "megastructure-sandbox"
    SANDBOX_IMAGE_TAG = "megastructure-sandbox-img:latest"

    def __init__(self):
        """Initialise l'extension et vérifie la disponibilité de Docker."""
        self.docker_client = None
        self.docker_available = False
        self.error_message = ""
        self.sandbox_data_path = None

        # Étape 2.1 : Définir et créer le dossier de données partagé pour la sandbox
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Remonte de PLATEFORMES -> EXTENSIONS -> LOGIQUES pour se placer à la racine de LOGIQUES
            logiques_folder = os.path.abspath(os.path.join(current_dir, '..', '..'))
            self.sandbox_data_path = os.path.join(logiques_folder, 'SANDBOX_DATA')
            os.makedirs(self.sandbox_data_path, exist_ok=True)
            print(f"[Universal Loader] Dossier de données de la sandbox assuré : {self.sandbox_data_path}")
        except Exception as e:
            self.error_message = f"Impossible de créer le dossier de la sandbox : {e}"
            print(f"[Universal Loader] ERREUR CRITIQUE: {self.error_message}")
            return # Arrêter l'initialisation si le dossier ne peut être créé

        try:
            # Tente de se connecter au daemon Docker avec un timeout
            self.docker_client = docker.from_env(timeout=5)
            # Vérifie que la connexion est active
            self.docker_client.ping()
            self.docker_available = True
            print("[Universal Loader] Connexion à l'API Docker réussie.")
        except ImportError:
            self.error_message = "La bibliothèque Docker n'est pas installée. Exécutez 'pip install docker'."
            print(f"[Universal Loader] ERREUR: {self.error_message}")
        except docker.errors.DockerException:
            self.error_message = "Le service Docker ne semble pas être en cours d'exécution. Veuillez le démarrer."
            print(f"[Universal Loader] ERREUR: {self.error_message}")
        except Exception as e:
            self.error_message = f"Erreur inattendue lors de la connexion à Docker: {e}"
            print(f"[Universal Loader] ERREUR: {self.error_message}")

    def execute(self, *args, **kwargs):
        """
        Méthode appelée pour exécuter l'extension. Pour l'instant, on se contente
        de retourner un message de succès.
        """
        return {
            "status": "success",
            "message": "L'extension Chargeur d'Applications Universel a été exécutée."
        }

    def get_sandbox_status(self):
        """Retourne le statut actuel de la sandbox (démarrée, arrêtée, etc.)."""
        if not self.docker_available:
            return {'status': 'error', 'message': self.error_message}
        
        try:
            container = self.docker_client.containers.get(self.SANDBOX_CONTAINER_NAME)
            status = container.status
            if status == "running":
                return {'status': 'running', 'message': f'Sandbox en cours d\'exécution (état: {status})'}
            else:
                # Si le conteneur existe mais n'est pas en cours d'exécution, on le nettoie.
                container.remove(force=True)
                return {'status': 'stopped', 'message': 'Sandbox arrêtée (nettoyage effectué).'}
        except docker.errors.NotFound:
            return {'status': 'stopped', 'message': 'Sandbox arrêtée.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur Docker: {e}'}

    def _start_container_thread(self, callback):
        """Thread worker pour démarrer le conteneur afin d'éviter de bloquer l'UI."""
        try:
            # 1. Nettoyer un éventuel conteneur précédent
            try:
                existing_container = self.docker_client.containers.get(self.SANDBOX_CONTAINER_NAME)
                print(f"[Universal Loader] Suppression de l'ancien conteneur '{self.SANDBOX_CONTAINER_NAME}'...")
                existing_container.remove(force=True)
            except docker.errors.NotFound:
                pass  # C'est le cas normal, on continue
            
            # 2. Construire l'image personnalisée si elle n'existe pas
            try:
                self.docker_client.images.get(self.SANDBOX_IMAGE_TAG)
                print(f"[Universal Loader] Image personnalisée '{self.SANDBOX_IMAGE_TAG}' trouvée.")
            except docker.errors.ImageNotFound:
                print(f"[Universal Loader] Image '{self.SANDBOX_IMAGE_TAG}' non trouvée. Construction en cours...")
                callback({'status': 'log', 'message': 'Image de la sandbox non trouvée. Construction en cours... (peut prendre plusieurs minutes)'})
                try:
                    dockerfile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docker')
                    image, build_log = self.docker_client.images.build(
                        path=dockerfile_dir,
                        tag=self.SANDBOX_IMAGE_TAG,
                        rm=True
                    )
                    for line in build_log:
                        if 'stream' in line: print(line['stream'].strip())
                    print("[Universal Loader] Construction de l'image terminée.")
                    callback({'status': 'log', 'message': 'Construction de l\'image terminée.'})
                except docker.errors.BuildError as e:
                    print(f"[Universal Loader] ERREUR de build Docker: {e}")
                    callback({'status': 'error', 'message': f'Erreur lors de la construction de l\'image Docker: {e}'})
                    return

            # 3. Démarrer le conteneur à partir de l'image personnalisée
            print(f"[Universal Loader] Démarrage du conteneur '{self.SANDBOX_CONTAINER_NAME}' depuis l'image '{self.SANDBOX_IMAGE_TAG}'...")
            container = self.docker_client.containers.run(
                self.SANDBOX_IMAGE_TAG,
                command="tail -f /dev/null",  # Commande pour garder le conteneur en vie
                name=self.SANDBOX_CONTAINER_NAME,
                detach=True,
                volumes={
                    self.sandbox_data_path: {'bind': '/data', 'mode': 'rw'}
                }
            )
            callback({'status': 'success', 'message': f'Sandbox démarrée avec l\'ID: {container.short_id}'})
        except Exception as e:
            callback({'status': 'error', 'message': f'Impossible de démarrer la sandbox: {e}'})

    def start_sandbox(self, callback):
        """Démarre l'environnement sandbox dans un thread séparé."""
        if not self.docker_available:
            callback({'status': 'error', 'message': self.error_message})
            return
        
        thread = threading.Thread(target=self._start_container_thread, args=(callback,))
        thread.start()

    def stop_sandbox(self, callback):
        """Arrête et supprime l'environnement sandbox."""
        if not self.docker_available:
            callback({'status': 'error', 'message': self.error_message})
            return
        
        try:
            print(f"[Universal Loader] Tentative d'arrêt du conteneur '{self.SANDBOX_CONTAINER_NAME}'...")
            container = self.docker_client.containers.get(self.SANDBOX_CONTAINER_NAME)
            container.stop()
            container.remove()  # Nettoie le conteneur après l'arrêt
            print(f"[Universal Loader] Conteneur '{self.SANDBOX_CONTAINER_NAME}' arrêté et supprimé.")
            callback({'status': 'success', 'message': 'Sandbox arrêtée avec succès.'})
        except docker.errors.NotFound:
            callback({'status': 'error', 'message': 'La sandbox n\'est pas en cours d\'exécution.'})
        except Exception as e:
            callback({'status': 'error', 'message': f'Impossible d\'arrêter la sandbox: {e}'})

    def list_sandbox_files(self):
        """Liste les fichiers présents dans la sandbox."""
        # Cette méthode liste les fichiers du volume partagé sur l'hôte.
        if not self.sandbox_data_path or not os.path.isdir(self.sandbox_data_path):
            return {'status': 'error', 'message': 'Le dossier de la sandbox est inaccessible.'}
        
        try:
            items = []
            for name in sorted(os.listdir(self.sandbox_data_path)):
                item_path = os.path.join(self.sandbox_data_path, name)
                item_type = 'folder' if os.path.isdir(item_path) else 'file'
                items.append({'name': name, 'type': item_type})
            return {'status': 'success', 'files': items}
        except Exception as e:
            return {'status': 'error', 'message': f'Impossible de lister les fichiers : {e}'}

    def upload_file_to_sandbox(self, host_file_path):
        """Téléverse un fichier depuis le système hôte vers la sandbox."""
        # Copie un fichier de l'hôte vers le volume partagé.
        if not host_file_path or not os.path.isfile(host_file_path):
            return {'status': 'error', 'message': 'Le fichier source est invalide ou n\'existe pas.'}

        if not self.sandbox_data_path:
            return {'status': 'error', 'message': 'Le dossier de la sandbox est inaccessible.'}

        try:
            filename = os.path.basename(host_file_path)
            destination_path = os.path.join(self.sandbox_data_path, filename)
            if os.path.exists(destination_path):
                return {'status': 'error', 'message': f'Un fichier nommé "{filename}" existe déjà dans la sandbox.'}
            shutil.copy2(host_file_path, destination_path)
            return {'status': 'success', 'message': f'Fichier "{filename}" téléversé dans la sandbox.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Impossible de téléverser le fichier : {e}'}

    def execute_in_sandbox(self, command):
        """Exécute une commande à l'intérieur du conteneur sandbox."""
        if not self.docker_available:
            return {'status': 'error', 'message': self.error_message}

        try:
            container = self.docker_client.containers.get(self.SANDBOX_CONTAINER_NAME)
            if container.status != 'running':
                return {'status': 'error', 'message': 'La sandbox n\'est pas en cours d\'exécution.'}

            # docker.exec_run retourne un tuple (exit_code, output)
            exit_code, output = container.exec_run(command)
            
            # Décode la sortie de bytes en string
            output_str = output.decode('utf-8').strip() if output else ""

            return {'status': 'success', 'exit_code': exit_code, 'output': output_str}

        except docker.errors.NotFound:
            return {'status': 'error', 'message': 'La sandbox n\'est pas en cours d\'exécution.'}
        except Exception as e:
            return {'status': 'error', 'message': f'Erreur Docker lors de l\'exécution: {e}'}