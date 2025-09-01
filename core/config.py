import os
import json

class AppConfig:
    def __init__(self, path):
        self.path = path
        self.data = {}
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    self.data = json.load(f)
                except Exception:
                    self.data = {}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)
