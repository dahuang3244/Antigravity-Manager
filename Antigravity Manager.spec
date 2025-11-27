# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gui\\main.py'],
    pathex=['gui'],
    binaries=[],
    datas=[('assets', 'assets'), ('gui', 'gui')],
    hiddenimports=['views', 'views.home_view', 'views.settings_view', 'account_manager', 'db_manager', 'process_manager', 'utils', 'theme', 'icons'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Antigravity Manager',
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
    icon=['assets\\icon.ico'],
)
