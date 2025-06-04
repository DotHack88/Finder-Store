# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['scraper.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\Emanuele\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\colorama', 'colorama')],
    hiddenimports=['colorama', 'requests', 'bs4', 'selenium'],
    hookspath=[],
    hooksconfig={},
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PS-Store-Scraper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icons8-play-station-310.ico'],
)
