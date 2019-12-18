#!/usr/bin/python3
#-*-coding:utf-8-*-

import readline
import sys
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
                pass

def format(sentence, length):

    for i in range(0, len(sentence)):
        print(sentence[i])


def main(useShm):

    global times
    while True:
        url = 'https://cn.bing.com/dict/search?q='

        try:
            if times != 1:
                word=str(input('> '))
                if not word or word.isspace():
                    continue
            else:
                word = sys.argv[0]

        except KeyboardInterrupt as e:
            sys.exit(0)
        except Exception as e:
            print(e)
            sys.exit(0)

        try:
            bt = bingTranslator();
            soup = bt.getSoup(url, word);
        except Exception:
            cprint('   No internet?', 'blue')
            continue

        headword = bt.getHeadword();
        if not headword:
            continue

        print()
        cprint('  ', end='')
        cprint(headword.string, 'yellow', attrs=['bold'])

        pronounciation, pronounciationUS = bt.getPronounciation()
        if pronounciation:
            cprint('   |', 'green', attrs=['bold'],end='')
            cprint('-- '+pronounciationUS.text.strip(),'green',attrs=['bold'], end='. ')
            cprint(pronounciation.text.strip(), 'green', attrs=['bold'])

        #词性(Part of speech)
        possf = bt.getPos()

        #翻译
        items = bt.getZhTran()


        print()
        poss,entrans = bt.getEnTran();
        for i in range(0,len(possf)):
            cprint('   '+possf[i].replace('.','')+
                    ': '+items[i].text.strip(), 'green')
            try:
                s = formatStr(entrans[poss[i]][0], 74, 7)

                if not s.isspace():
                    cprint('     |', color='cyan')

                s = s[:5] + '|_' + s[7:]
                cprint(s, color='cyan')
                print()

            except IndexError:
                print()
                continue


        words = bt.getOtherWordForms();

        if words != []:
            print()
            cprint('   '+str(words), 'magenta')
            print()

        audio = bt.getAudioLink()
        try:
            #cprint('   '+audio[0], 'cyan')
            #cprint('   '+audio[1], 'cyan')
            pass
        except Exception:
            pass

        if times == 1:
            sys.exit(0)

main(useShm)
