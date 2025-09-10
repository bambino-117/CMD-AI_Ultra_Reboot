# Megastructure.spec

a = Analysis(
    ['conteneur_monde.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('INTERFACES/templates', 'INTERFACES/templates'),
        ('INTERFACES/static', 'INTERFACES/static'),
        ('INTERFACES/config.json', 'INTERFACES'),
        ('LOGIQUES/CONTENEURS', 'LOGIQUES/CONTENEURS'),
        ('LOGIQUES/EXTENSIONS', 'LOGIQUES/EXTENSIONS'),
        ('RESSOURCES', 'RESSOURCES'),
        ('tester_codes.json', '.'),
        ('.env', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Megastructure',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # True pour voir les logs de la console au lancement
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # NOUVEAU: Icône de l'application (optionnel, à créer)
    # icon='path/to/your/icon.ico' # pour Windows
    # icon='path/to/your/icon.icns' # pour macOS
)

# Pour macOS, créer un .app bundle
app = BUNDLE(
    exe,
    name='Megastructure.app',
    icon=None, # Mettre le chemin de l'icône .icns ici
    bundle_identifier=None,
)
