#!/usr/bin/python3
#-*-coding:utf-8-*-

import readline
import sys
import re
import requests
import time
from bs4 import BeautifulSoup
from termcolor import colored, cprint
from bing.BingTran import bingTranslator
from bing.strctl import formatStr

if __name__ == "__main__":
    #共享内存使用标识
    useShm = 0
    times = 0
    sys.argv.remove(sys.argv[0])
    if len(sys.argv) >= 1:
        for arg in sys.argv:
            if arg == '-s':
                print('Using SharedMemory')
                useShm = 1
            else:
                times = 1

def isword(src):
    result = re.findall(r'\w+', src);
    return len(result) <= 1

def doNothing():
    pass


def main(useShm):

    global times
    actualStart = 10
    bt = bingTranslator();
    shm = bt.connect_shared_memory() if useShm else doNothing()

    while True:
        url = 'https://cn.bing.com/dict/search?q='
        string = ""

        try:
            if times != 1:
                src=str(input('> '))
                if not src or src.isspace():
                    continue
                if not isword(src):
                    cprint('    Not a src', 'blue')
                    continue
            else:
                src = sys.argv[0]

        except KeyboardInterrupt as e:
            sys.exit(0)
        except Exception as e:
            print(e)
            continue

        try:
            soup = bt.getSoup(url, src);
        except Exception as e:
            cprint('   '+str(e))
            cprint('   No internet?', 'blue')
            continue

        headword = bt.getHeadword();
        if not headword:
            continue

        print() if not useShm else doNothing()
        cprint('  ', end='') if not useShm else doNothing()
        cprint(headword.string, 'yellow', attrs=['bold']) if not useShm else doNothing()
        string += headword.string +' |'

        pronunciation, pronunciationUS = bt.getpronunciation()
        if pronunciation:
            cprint('   |', 'green', attrs=['bold'],end='') if not useShm else doNothing()
            cprint('-- '+pronunciationUS.text.strip(),'green',attrs=['bold'], end='. ') if not useShm else doNothing()
            cprint(pronunciation.text.strip(), 'green', attrs=['bold']) if not useShm else doNothing()
            string += '    '+pronunciationUS.text.strip() + '  ' + pronunciation.text.strip() + '|'
        else: 
            string += '|'

        #词性(Part of speech)
        possf = bt.getPos()

        #翻译
        items = bt.getZhTran()


        print() if not useShm else doNothing()
        poss,entrans = bt.getEnTran();
        for i in range(0,len(possf)):
            cprint('   '+possf[i].replace('.','')+
                    ': '+items[i], 'green') if not useShm else doNothing()
            string += possf[i] + items[i] + '|'
            try:
                s = formatStr(entrans[poss[i]][0], 74, 7)

                if not s.isspace():
                    cprint('     |', color='cyan') if not useShm else doNothing()

                s = s[:5] + '|_' + s[7:]
                cprint(s, color='cyan') if not useShm else doNothing()
                print() if not useShm else doNothing()

            except IndexError:
                print() if not useShm else doNothing()
                continue

        try:
            noEnTran = 1
            for i in range(0,len(possf)):
                if entrans[poss[i]][0]:
                    string += entrans[poss[i]][0] + '|'
                    noEnTran = 0
        except Exception:
            string += '|' if noEnTran else ''
            pass


        words = bt.getOtherWordForms();

        if words != []:
            print() if not useShm else doNothing()
            cprint('   '+str(words), 'magenta') if not useShm else doNothing()
            string += str(words)
            print() if not useShm else doNothing()

        string += '|'

        audio = bt.getAudioLink()
        try:
            string += audio[0] + '|'
            string += audio[1] + '|'
            pass
        except Exception:
            pass

        if times == 1:
            sys.exit(0)

        cprint(string, 'green') if useShm else doNothing()
        cprint(bt.getConcatenateFlag(), 'green') if useShm else doNothing()

        shm.write(string, actualStart) if useShm else doNothing()
        shm.write(bt.getConcatenateFlag(), 0) if useShm else doNothing()

main(useShm)
