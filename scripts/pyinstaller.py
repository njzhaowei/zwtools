import os
import platform
import shutil
import sys
from subprocess import Popen
from pathlib import Path

try:
    import PyInstaller
except ImportError:
    PyInstaller = None
    raise SystemExit('Error: PyInstaller package missing. '
                     'To install type: pip install --upgrade pyinstaller')

IS_WIN = platform.system() == 'Windows'
IS_MAC = platform.system() == 'Darwin'
IS_LNX = platform.system() == 'Linux'

EXE_EXT = ''
PYI_SPEC = ''
if IS_WIN:
    EXE_EXT = '.exe'
    PYI_EXE = '.\\.venv\\Scripts\\pyinstaller.exe'
    PYI_SPEC = 'pyinstaller_win.spec'
elif IS_MAC:
    EXE_EXT = '.app'
    PYI_EXE = './.venv/bin/pyinstaller'
    PYI_SPEC = 'pyinstaller_mac.spec'
elif IS_LNX:
    EXE_EXT = ''
    PYI_EXE = './.venv/bin/pyinstaller'
    PYI_SPEC = 'pyinstaller_linux.spec'

# PYI_SPEC = 'pyinstaller_win_onefile.spec'

DIST_DIR    = Path('./tmp/dist')
BUILD_DIR   = Path('./tmp/build')
UPX_DIR     = Path('./bin') # get upx from https://upx.github.io/

PRJ_NAME = Path(os.path.abspath(__file__)).parent.parent.name
APP_NAME = PRJ_NAME

def main():
    '''
    --debug: embed debug info into exe and set to Console app
    --console: Console app (Default not set)
    --onefile: One file exe
    -specfile: Spec file path
    -upxdir: UPX bin dir
    -o: Output app name
    '''

    # Platforms supported
    if platform.system() not in ['Windows', 'Darwin', 'Linux']:
        raise SystemExit('Error: Only Windows, Linux and Darwin platforms are '
                         'currently supported.')

    # Clean
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    shutil.rmtree('./__pycache__', ignore_errors=True)
    # Prepare dirs
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # Execute pyinstaller.
    # Note: the '--clean' flag passed to PyInstaller will delete
    #       global global cache and temporary files from previous
    #       runs. For example on Windows this will delete the
    #       '%appdata%/Local/pyinstaller/bincache00_py37_64bit'
    #       or
    #       '%appdata%/roaming/pyinstaller/bincache00_py37_64bit'
    #       directory.
    env = os.environ
    av = sys.argv

    global APP_NAME
    if '-o' in av:
        for i in range(len(av)):
            if av[i] == '-o':
                APP_NAME = av[i+1]
                break

    global UPX_DIR
    if '-upxdir' in av:
        for i in range(len(av)):
            if av[i] == '-upxdir':
                UPX_DIR = Path(av[i+1])
                break

    global PYI_SPEC
    if '-specfile' in av:
        for i in range(len(av)):
            if av[i] == '-specfile':
                PYI_SPEC = av[i+1]
                break

    env['PYINSTALLER_APPNAME'] = APP_NAME
    if '--debug' in av:
        env['PYINSTALLER_DEBUG'] = '1'
    if '--console' in av:
        env['PYINSTALLER_CONSOLE'] = '1'
    if '--debug' in av and '--console' not in av:
        env['PYINSTALLER_CONSOLE'] = '1'
    if UPX_DIR.exists():
        env['PYINSTALLER_UPX'] = '1'
    if '--onefile' in av:
        env['PYINSTALLER_ONEFILE'] = '1'

    args = [
        PYI_EXE, '--clean',
        '--distpath', str(DIST_DIR),
        '--workpath', str(BUILD_DIR),
    ]
    if UPX_DIR.exists():
        args.extend(['--upx-dir', str(UPX_DIR)])
    args.append(PYI_SPEC)

    print('CMD: ', ' '.join(args))
    sub = Popen(args=args, env=env)
    sub.communicate()
    rcode = sub.returncode
    if rcode != 0:
        print('Error: PyInstaller failed, code=%s' % rcode)
        # Delete distribution directory if created
        shutil.rmtree(DIST_DIR, ignore_errors=True)
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
        sys.exit(1)

    # Make sure everything went fine
    appdir = DIST_DIR/APP_NAME if 'PYINSTALLER_ONEFILE' not in env else DIST_DIR
    executable = appdir/(APP_NAME+EXE_EXT)
    if not executable.exists():
        print('Error: PyInstaller failed, main executable is missing: %s' % executable)
        sys.exit(1)

    # Clean
    shutil.rmtree('./__pycache__', ignore_errors=True)

    print('*'*80)
    print('PYINSTALLER_DEBUG:', env['PYINSTALLER_DEBUG']=='1' if 'PYINSTALLER_DEBUG' in env else False)
    print('PYINSTALLER_CONSOLE:', env['PYINSTALLER_CONSOLE']=='1' if 'PYINSTALLER_CONSOLE' in env else False)
    print('UPX DIR:', UPX_DIR.resolve())
    print('PYINSTALLER_UPX:', env['PYINSTALLER_UPX']=='1' if 'PYINSTALLER_UPX' in env else False)
    print('PYINSTALLER_APPNAME:', env['PYINSTALLER_APPNAME'])
    print('PYINSTALLER_ONEFILE:', env['PYINSTALLER_ONEFILE']=='1' if 'PYINSTALLER_ONEFILE' in env else False)

    # Done
    print('PyInstaller Finish.')

    # On Windows open folder in explorer or when --debug is passed
    # run the result binary using 'cmd.exe /k cefapp.exe', so that
    # console window doesn't close.
    if IS_WIN:
        if '--debug' in sys.argv:
            os.system('cd %s && start cmd /k "%s"' % (appdir.resolve(), executable.resolve()))
        else:
            # SYSTEMROOT = C:/Windows
            os.system('%s/explorer.exe /n,/e,"%s"' % (os.environ['SYSTEMROOT'], appdir))

if __name__ == '__main__':
    main()
