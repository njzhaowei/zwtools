# -*- mode: python -*-
# -*- coding: utf-8 -*-

"""
This is a PyInstaller spec file.
"""

import os
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.utils.hooks import is_module_satisfies
from PyInstaller.archive.pyz_crypto import PyiBlockCipher

# Constants
APPNAME = os.environ.get("PYINSTALLER_APPNAME", 'zwapp')
DEBUG   = os.environ.get("PYINSTALLER_DEBUG", False)
CONSOLE = os.environ.get("PYINSTALLER_CONSOLE", False)
UPX     = os.environ.get("PYINSTALLER_UPX", False)
ONEFILE = os.environ.get("PYINSTALLER_ONEFILE", False)
PYCRYPTO_MIN_VERSION = "2.6.1"
LOGO    = "../res/logo.ico"

# Set this secret cipher to some secret value. It will be used
# to encrypt archive package containing your app's bytecode
# compiled Python modules, to make it harder to extract these
# files and decompile them. If using secret cipher then you
# must install pycrypto package by typing: "pip install pycrypto".
# Note that this will only encrypt archive package containing
# imported modules, it won't encrypt the main script file
# (wxpython.py). The names of all imported Python modules can be
# still accessed, only their contents are encrypted.
SECRET_CIPHER = "This-is-a-secret-phrase"  # Only first 16 chars are used
SECRET_CIPHER = None
# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

if SECRET_CIPHER:
    # If using secret cipher then pycrypto package must be installed
    if not is_module_satisfies("pycrypto >= %s" % PYCRYPTO_MIN_VERSION):
        raise SystemExit("Error: pycrypto %s or higher is required. "
                         "To install type: pip install --upgrade pycrypto"
                         % PYCRYPTO_MIN_VERSION)
    cipher_obj = PyiBlockCipher(key=SECRET_CIPHER)
else:
    cipher_obj = None

a = Analysis(
    ["../main.py"],
    datas=[('../conf', './conf')],
    pathex=[],
    binaries=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["pyinstaller_hook.py"],
    excludes=[],
    win_no_prefer_redirects=True,
    win_private_assemblies=True,
    noarchive=False,
    cipher=cipher_obj
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=cipher_obj
)

if ONEFILE:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,  
        [],
        name=APPNAME,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=UPX,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=CONSOLE,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=LOGO
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        exclude_binaries=True,
        name=APPNAME,
        debug=DEBUG,
        strip=False,
        upx=UPX,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=CONSOLE,
        icon=LOGO
    )

    COLLECT(exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            strip=False,
            upx=UPX,
            name=APPNAME)
