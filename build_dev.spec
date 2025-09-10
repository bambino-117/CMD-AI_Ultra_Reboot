# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['conteneur_monde.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('INTERFACES', 'INTERFACES'),
        ('LOGIQUES', 'LOGIQUES'),
        ('RESSOURCES', 'RESSOURCES'),
        ('tester_codes.json', '.'),
        ('.env', '.')
    ],
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
    name='CMD-AI-DEV',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # Console visible pour le build de développement
    icon='RESSOURCES/icons/CMD-AI_Ultra_main.ico',
)
coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name='CMD-AI-DEV'
)