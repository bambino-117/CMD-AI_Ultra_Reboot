# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Liste des fichiers et dossiers à inclure depuis INTERFACES/templates
# On exclut explicitement le dossier 'admin'
public_templates_items = [
    item for item in os.listdir('INTERFACES/templates') if item != 'admin'
]

datas_list = [
    ('INTERFACES/static', 'INTERFACES/static'),
    ('INTERFACES/config.example.json', 'INTERFACES'),
    ('LOGIQUES', 'LOGIQUES'),
    ('RESSOURCES', 'RESSOURCES'),
]

# Ajoute chaque fichier/dossier public des templates à la liste des données
for item in public_templates_items:
    source_path = os.path.join('INTERFACES/templates', item)
    dest_path = os.path.join('INTERFACES', 'templates')
    datas_list.append((source_path, dest_path))


a = Analysis(
    ['conteneur_monde.py'],
    pathex=['.'],
    binaries=[],
    datas=datas_list,
    hiddenimports=['pkg_resources.py2_warn'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CMD-AI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # Pas de console pour le build public
    icon='RESSOURCES/icons/CMD-AI_Ultra_main.ico',
)
coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name='CMD-AI'
)