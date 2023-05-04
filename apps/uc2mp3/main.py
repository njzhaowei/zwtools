import os
import sys
import getopt
import traceback
import struct
import json
import eyed3

from pathlib import Path
from tqdm import tqdm
from zwtk.fileutils import dirsize, readbin, writebin
from zwtk.comm import waitkey
from zwtk.zwsqlite import ZWSqlite

EXE_PTH = Path(sys.argv[0]).resolve()
CWD_DIR = Path(sys.argv[0]).parent.resolve()
TMP_DIR = Path(__file__).parent.parent.resolve()
MEI_TMP = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path('.')
SRC_DIR = CWD_DIR
DB_PATH = None

def usage():
    print('Desc: Change *.uc from Netease CloudMusic to mp3.\n'+
        'Search webdb.dat to set mp3 file name and ID3 info\n'+
        'Usage: \n'+
        '{0} #use current directory as source directory\n'+
        '{0} -d ucfile_dirpath\n'+
        '{0} -w webdb.dat_filepath'.format(EXE_PTH.name)
    )

def crack_ucfile(inpth, outpth):
    ctn = readbin(inpth)
    arr = []
    s = struct.Struct('<B')
    for i in tqdm(range(len(ctn)), ascii=True):
        b = ctn[i]
        b = b ^ 163
        a = s.pack(b)
        arr.append(a)
    writebin(outpth, b''.join(arr))

def get_webdb():
    global DB_PATH
    webdbpth = Path(os.getenv('USERPROFILE')) / ('AppData/Local/Netease/CloudMusic/Library/webdb.dat') if DB_PATH is None else DB_PATH
    return webdbpth if webdbpth.exists() else None

def get_song(dbpth, ucid):
    rec = None
    tid = ucid.split('-')[0]
    with ZWSqlite(str(dbpth)) as db:
        rec = db.findone('web_track', tid=tid)
    return json.loads(rec.track) if rec else None

def main():
    try:
        usage()
        print('Exe path: %s, Unpack size: %.2fM'%( MEI_TMP, (dirsize(MEI_TMP)/1024/1024) ))
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hd:w:', ['help', 'dir', 'webdb'])
        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            usage()
            sys.exit(2)

        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
                sys.exit()
            elif o in ('-d', '--dir'):
                global SRC_DIR
                SRC_DIR = Path(a)
            elif o in ('-d', '--webdb'):
                global DB_PATH
                DB_PATH = Path(a)
            else:
                assert False, "unhandled option"

        pths = list(SRC_DIR.glob('**/*.uc'))
        pthlen = len(pths)
        webdb = get_webdb()
        for idx, pth in enumerate(pths):
            print('Process (%d/%d) %s'%(idx+1, pthlen, pth.name))
            songname = pth.stem
            songinfo = None
            if webdb:
                songinfo = get_song(webdb, pth.stem)
                if songinfo:
                    songartists = '&'.join([o['name'] for o in songinfo['artists']])
                    songname = '%s - %s'%( songinfo['name'], songartists )
            songpath = pth.parent/('%s.mp3'%songname)
            print('Save to %s'%songpath)
            crack_ucfile(pth, songpath)
            if songinfo:
                audiofile = eyed3.load(songpath)
                audiofile.tag.title = songinfo['name']
                audiofile.tag.artist = ';'.join([o['name'] for o in songinfo['artists']])
                audiofile.tag.album = songinfo['album']['name'] if 'album' in songinfo else None
                audiofile.tag.save()
    
    except Exception:
        traceback.print_exc()

    print('Press any key to continue...')
    waitkey()

if __name__ == '__main__':
    main()
