#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.realpath(__file__)), **kwargs)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"CMD-AI Ultra Reboot V3 démarré sur http://localhost:{PORT}")
        print("Ouverture du navigateur...")
        webbrowser.open(f'http://localhost:{PORT}/Interface.html')
        print("Appuyez sur Ctrl+C pour arrêter le serveur")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServeur arrêté.")
            sys.exit(0)