import sys
import warnings
import re
import urllib
import sysv_ipc as ipc
from termcolor import cprint
from bs4 import BeautifulSoup

class bingTranslator(object):
    def __init__(self):
        self.soup = None
        self.response = None

        self.finish = '0'
        self.phonetic = '0'
        self.zhTranNum = '0'
        self.enTranNum = '0'
        self.otherWordFormFlag = '0'
        self.audioNum = '0'
        pass

    def getConcatenateFlag(self):

        self.finish = '1'
        flag = self.finish + self.phonetic + self.zhTranNum +\
                self.enTranNum + self.otherWordFormFlag + \
                self.audioNum
        
        return flag


    def clearFlag(self):

        self.finish = '0'
        self.phonetic = '0'
        self.zhTranNum = '0'
        self.enTranNum = '0'
        self.otherWordFormFlag = '0'
        self.audioNum = '0'


    def connect_shared_memory (self):

        warnings.simplefilter("ignore")
        path = "/tmp"
        projectID = 2334
        try:
            key = ipc.ftok(path, projectID)
            shm = ipc.SharedMemory(key, 0, 0)
            shm.attach(0,0)
        except Exception as e:
            print('bing 获取共享内存失败'+str(e))
            sys.exit(1)

        return shm

    def getHeaders (self):

        headers = {
                "authority":"cn.bing.com",
                "method":"GET",
                "accept-encoding":"gzip",
                "user-agent":"Mozilla/5.0",
                "cookie":"ipv6=hit=1565876084714&t=4;",
                "dnt": '1',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                }

        return headers

    def getResponse (self, url, word):
        try:
            url += urllib.parse.quote_plus(word)
            response = urllib.request.Request(url, headers=self.getHeaders())
            response = urllib.request.urlopen(url)
        except KeyboardInterrupt:
            print('Good bye~')
            exit(0)

        self.response = response
        return response

    def getSoup(self, url, word): 
        self.response = self.getResponse(url, word)
        self.soup = BeautifulSoup(self.response, 'html.parser')
        return self.soup

    def getHeadword(self):
        return self.soup.find('div', { 'class':'hd_div', 'id':'headword' })

    def getpronunciation(self):

        #音标pronociation: 英音 & 美音
        pronunciationUS = self.soup.find('div', { 'class':'hd_prUS' })
        pronunciation = self.soup.find('div', { 'class':'hd_pr' })

        if pronunciation or pronunciationUS:
            self.phonetic = '1'

        return pronunciation, pronunciationUS

    def getPos(self):
        poss = []
        for pos in self.soup.findAll('span', { 'class':'pos' }):
            pos.string = pos.string.replace('网络', "网络.")
            poss.append(pos.string)

        return poss

    def getZhTran(self):
        items = []
        num = 0
        for i in self.soup.findAll('span', { 'class':'def' }):

            #不要直接使用.string，否则span里的内容可能无法提取出来
            items.append(i.text)
            num = num + 1

        self.zhTranNum = str(num)
        return items

    def getAudioLink(self):
        #语音
        audios = self.soup.findAll('div', { 'class':'hd_tf' })
        link = []
        for audio in audios:
            link.append(re.search(r'https\:\/\/.+?\.mp3', str(audio)).group(0))

        self.audioNum = str(len(link))

        return link

    def getOtherWordForms(self):

        try:
            content = self.soup.find('div', { 'class':'hd_if' })
            words = []
            span = content.findAll('span')
            a = content.findAll('a')
        except Exception:
            return words

        for i,s in enumerate(span):
            part = s.string.replace('：',': ') + a[i].string
            words.append(part)

        self.otherWordFormFlag = '1' if words != [] else '0'

        return words

    def getEnTran(self):

        try:
            whold = self.soup.find('div' , { 'id':'homoid' })
            divs = whold.findAll('tr', { 'class':'def_row df_div1' })
        except Exception:
            return [], []

        pos = []
        data = {}

        for div in divs:
            p = div.find('div', { 'class':'pos pos1' }).string
            pos.append(p)

        for i,item in enumerate(divs):
            result = item.findAll('div',{ 'class' :'de_li1 de_li3' })
            sentences = []
            for block in result:
                discrete = block.find('div', { 'class':'df_cr_w' }).findAll('a')
                sentence = ""
                for word in discrete:
                    sentence += word.string  + ' '

                sentences.append(sentence)

            data[pos[i]] = sentences

        self.enTranNum = str(1) if len(data) > 0 else str(0)
        return pos,data
