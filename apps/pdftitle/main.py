import os,sys
import getopt
import traceback
import psutil

from pathlib import Path
from PyPDF2 import PdfReader, PdfMerger
from zwutils.fileutils import dirsize
from zwutils.comm import waitkey

EXE_PTH = Path(sys.argv[0]).resolve()
CWD_DIR = Path(sys.argv[0]).parent.resolve()
TMP_DIR = Path(__file__).parent.parent.resolve()
MEI_TMP = Path(sys._MEIPASS)
DST_DIR = CWD_DIR

def usage():
    print('Desc: Set pdf title from file name.\nUsage: \n{0} #use current dir as target_dir\n{0} -d target_dir'.format(EXE_PTH.name))

def main():
    try:
        mem = psutil.virtual_memory()
        rss = psutil.Process(os.getpid()).memory_info().rss
        print('Unpack size: %.2fM, Mem: %0.2fM/%0.2fM'%( (dirsize(MEI_TMP)/1024/1024), rss/1024/1024, mem.total/1024/1024 ))
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hd:', ['help', 'dir'])
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
                global DST_DIR
                DST_DIR = Path(a)
            else:
                assert False, "unhandled option"

        pths = list(DST_DIR.glob('**/*.pdf'))
        pthlen = len(pths)
        for idx, pth in enumerate(pths):
            print('Process (%d/%d) %s'%(idx+1, pthlen, pth.name))
            file_in = open(pth, 'rb')
            pdf_reader = PdfReader(file_in)
            metadata = pdf_reader.metadata
            print(metadata)

            pdf_merger = PdfMerger()
            pdf_merger.append(file_in)
            pdf_merger.add_metadata({
                '/Title': pth.stem
            })
            file_out_pth = pth.parent / ('%s_out.pdf'%pth.stem)
            file_out = open(file_out_pth, 'wb')
            pdf_merger.write(file_out)

            file_in.close()
            file_out.close()

            pth.unlink()
            file_out_pth.rename(pth)

    except Exception:
        traceback.print_exc()

    print('Press any key to continue...')
    waitkey()

if __name__ == '__main__':
    main()
