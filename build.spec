# -*- mode: python ; coding: utf-8 -*-
# https://pyinstaller.readthedocs.io/en/stable/spec-files.html
block_cipher = None
PROJECT_NAME = "the_stars_came_down_screaming"

a = Analysis(
    ["main.py"],
    binaries=[],
    datas=[
        ("data", "data"),
        ("saves", "saves")
    ],
    hiddenimports=[],
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
    name=PROJECT_NAME,  # Name of the executable.
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to False to disable the Windows terminal.
    icon="icon.ico",  # Windows icon file.
    onefile=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=PROJECT_NAME,  # Name of the distribution directory.
)
