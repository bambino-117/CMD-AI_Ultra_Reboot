import docker
import os
import tarfile
import io
from LOGIQUES.EXTENSIONS.base_extension import BaseExtension

class UniversalLoaderExtension(BaseExtension):
    """
    Extension pour gérer une sandbox Docker.
    Permet de démarrer, arrêter, et interagir avec un conteneur isolé.
    """
    NAME = "Chargeur d'Applications Universel"
    DESCRIPTION = "Sandbox Docker pour applications isolées."

    CONTAINER_NAME = "megastructure-sandbox"
    IMAGE_NAME = "megastructure-sandbox-img"

    def __init__(self, sandbox_api):
        """Initialise l'extension et le client Docker."""
        super().__init__(sandbox_api)
        self.docker_client = None
        try:
            self.docker_client = docker.from_env()
            # Vérifie la connexion Docker au démarrage
            self.docker_client.ping()
            self.sandbox.log("Client Docker initialisé et connecté.")
        except Exception:
            self.sandbox.log("Erreur: Docker n'est pas en cours d'exécution ou est mal configuré.")
            self.docker_client = None

    def _get_container(self):
        """Récupère l'objet conteneur s'il existe."""
        if not self.docker_client:
            return None
        try:
            return self.docker_client.containers.get(self.CONTAINER_NAME)
        except docker.errors.NotFound:
            return None

    def _build_image_if_needed(self, callback=None):
        """Construit l'image Docker si elle n'existe pas, en streamant les logs."""
        if not self.docker_client:
            return False
        try:
            self.docker_client.images.get(self.IMAGE_NAME)
            self.sandbox.log(f"Image Docker '{self.IMAGE_NAME}' déjà présente.")
            return True
        except docker.errors.ImageNotFound:
            self.sandbox.log(f"Image Docker '{self.IMAGE_NAME}' non trouvée. Construction en cours...")
            dockerfile_path = os.path.dirname(__file__)
            try:
                stream = self.docker_client.api.build(path=dockerfile_path, tag=self.IMAGE_NAME, rm=True, decode=True)
                for chunk in stream:
                    if 'stream' in chunk:
                        log_line = chunk['stream'].strip()
                        if log_line and callback:
                            callback({'status': 'log', 'message': log_line})
                self.sandbox.log("Image Docker construite avec succès.")
                return True
            except Exception as e:
                error_message = f"Erreur lors de la construction de l'image Docker : {e}"
                self.sandbox.log(error_message)
                if callback:
                    callback({'status': 'error', 'message': error_message})
                return False

    def get_sandbox_status(self):
        """Retourne le statut actuel de la sandbox."""
        container = self._get_container()
        if container and container.status == 'running':
            try:
                # Le port interne 6080 est pour websockify
                assigned_port = container.ports.get('6080/tcp')[0]['HostPort']
                return {'status': 'running', 'sandbox_status': container.status, 'vnc_port': assigned_port}
            except (TypeError, IndexError, KeyError):
                return {'status': 'running', 'sandbox_status': container.status, 'vnc_port': None, 'message': 'Conteneur actif mais port VNC non trouvé.'}
        return {'status': 'inexistant', 'sandbox_status': 'inexistant'}

    def start_sandbox(self, callback):
        """Démarre la sandbox Docker."""
        if not self.docker_client:
            return callback({'status': 'error', 'message': "Le client Docker n'est pas disponible."})

        if not self._build_image_if_needed(callback):
            return

        container = self._get_container()
        if container and container.status == 'running':
            container.reload()
            try:
                assigned_port = container.ports['6080/tcp'][0]['HostPort']
                return callback({'status': 'success', 'sandbox_status': 'running', 'message': 'La sandbox est déjà en cours d\'exécution.', 'vnc_port': assigned_port})
            except (TypeError, IndexError, KeyError):
                 return callback({'status': 'error', 'message': 'Sandbox active mais port VNC inaccessible.'})

        try:
            self.sandbox.log("Démarrage du conteneur sandbox...")
            ports = {'6080/tcp': None}

            self.docker_client.containers.run(
                self.IMAGE_NAME,
                detach=True,
                name=self.CONTAINER_NAME,
                extra_hosts={"host.docker.internal": "host-gateway"},
                ports=ports,
                remove=True
            )
            
            container = self._get_container()
            container.reload()
            assigned_port = container.ports['6080/tcp'][0]['HostPort']
            self.sandbox.log(f"Conteneur démarré. VNC accessible sur le port hôte : {assigned_port}")

            callback({'status': 'success', 'sandbox_status': 'running', 'message': f'Sandbox démarrée.', 'vnc_port': assigned_port})
        except Exception as e:
            callback({'status': 'error', 'message': f"Erreur au démarrage de la sandbox : {e}"})

    def stop_sandbox(self, callback):
        """Arrête et supprime la sandbox Docker."""
        container = self._get_container()
        if not container:
            return callback({'status': 'success', 'sandbox_status': 'inexistant', 'message': 'La sandbox n\'est pas en cours d\'exécution.'})
        try:
            self.sandbox.log("Arrêt du conteneur sandbox...")
            container.stop()
            container.remove()
            callback({'status': 'success', 'sandbox_status': 'inexistant', 'message': 'Sandbox arrêtée et supprimée.'})
        except Exception as e:
            callback({'status': 'error', 'message': f"Erreur à l'arrêt de la sandbox : {e}"})

    def upload_file_to_sandbox(self, host_file_path):
        """Téléverse un fichier de l'hôte vers la sandbox."""
        container = self._get_container()
        if not container or container.status != 'running':
            return {'status': 'error', 'message': 'La sandbox n\'est pas en cours d\'exécution.'}

        dest_path = "/sandbox_files/"
        filename = os.path.basename(host_file_path)
        
        pw_tarstream = io.BytesIO()
        with tarfile.open(fileobj=pw_tarstream, mode='w') as tar:
            tar.add(host_file_path, arcname=filename)
        pw_tarstream.seek(0)

        try:
            container.put_archive(path=dest_path, data=pw_tarstream)
            self.sandbox.log(f"Fichier '{filename}' téléversé dans la sandbox.")
            return {'status': 'success', 'message': f"Fichier '{filename}' téléversé avec succès."}
        except Exception as e:
            self.sandbox.log(f"Erreur de téléversement : {e}")
            return {'status': 'error', 'message': f"Erreur lors du téléversement : {e}"}

    def execute(self, *args, **kwargs):
        """Action par défaut de l'extension."""
        return {'status': 'info', 'message': 'Les actions de cette extension sont gérées via ses méthodes spécifiques.'}