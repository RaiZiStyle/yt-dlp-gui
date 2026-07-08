# yt-dlp-gui.spec
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        # Si tu as des fichiers de ressources (icônes, etc.)
        # ('src/assets', 'assets'),
    ],
    hiddenimports=[
        *collect_submodules('yt_dlp'),
        *collect_submodules('websockets'),  # yt_dlp l'utilise pour le streaming
        'certifi',
        'requests',
        'PySide6',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='yt-dlp-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,      # ← False = pas de fenêtre console (équivalent à --windowed)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='src/assets/icon.ico',  # ← décommente si tu as une icône
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='yt-dlp-gui',
)