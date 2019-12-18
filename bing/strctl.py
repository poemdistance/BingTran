#!/usr/bin/python3

def formatStr(sentence, length, spaceSize):

    start = 0
    space = ''
    for i in range(spaceSize):
        space += ' '

    i = 0
    result = space
    times = 1

    while i < len(sentence):
        result += sentence[i]
        i = i + 1
        if i-start == length:
            if i<len(sentence) and sentence[i] == ' ':
                result += ' '+'\n'+ space #空格置于句尾
                times = times + 1
                i = i + 1          #复制空格后向后移移位
                start = i
            else:
                tmp = i
                while sentence[i] != ' ':
                    i = i - 1;

                    #回溯到起点，恢复分割点下标强制分割
                    if i == start:
                        i = tmp - 1 #抵消切片中的i+1,使其复制本身
                        break


                #while在空格退出,切片终点是数值-1，所以i需+1抵消才能复制到空格
                result = result[:i+1+spaceSize*times]

                #空格已经复制，i+1使其下一次复制被跳过
                i = i + 1
                start = i + 1
                result += '\n' + space
                times = times + 1


    return result



if __name__ == '__main__':
    s = formatStr("Here’s what you’ll learn in this tutorial: Python provides a rich set of operators, functions, and methods for working with strings. When you are finished with this tutorial, you will know how to access and extract portions of strings, and also be familiar with the methods that are available to manipulate and modify string data. ", 44, 7);

    print(s)
