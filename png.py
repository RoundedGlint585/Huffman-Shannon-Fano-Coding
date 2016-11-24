from __future__ import print_function
from PIL import Image
from numpy.lib.scimath import log2
from operator import itemgetter

def get_seq():
    #Image.open("temp.jpg").convert("L").save("tes.jpg")
    image = Image.open("test.jpg")#загружаем енотиков
    print(image.format, image.size, image.mode)#Проверяем формат
    width = image.size[0] #Определяем ширину.
    height = image.size[1] #Определяем высоту.
    source = image.load() #Выгружаем пиксели
    message = [] #Список для элементов
    for i in range (width):
         message.append(round(float(source[i,height/2])/20)*20)
    #message.sort()
    return message

def Entropy_value(frequency, length):
    entropy = 0
    for i in frequency:
        entropy -= (frequency[i]/length* log2(frequency[i]/length))
    return entropy

def Shannon_Fano_coding(seq, code):
    a = {}
    b = {}
    if len(seq) == 1:
        print(seq.popitem()[0],  "=>" , code)
        return 0
    for i in sorted(seq.items(), key=itemgetter(1), reverse=True):
        if sum(a.values()) < sum(b.values()):
            a[i[0]] = seq[i[0]]
        else:
            b[i[0]] = seq[i[0]]
    Shannon_Fano_coding(a, code + "0")
    Shannon_Fano_coding(b, code + "1")

def Huffman_coding(seq):
    code = dict.fromkeys(seq.keys(), "")
    seq = sorted(seq.items(), key=itemgetter(1))
    tree = []
    for i in seq:
        temp = []
        l = []
        l.append(i[0])
        temp.append(i[1])
        temp.append(l)
        tree.append(temp)
    while len(tree) != 1:
        tree.sort()
        for i in tree[0][1]:
            code[i] += "0"
        for i in tree [1][1]:
            code[i] += "1"
        tree[1][0] += tree[0][0]
        tree[1][1].extend(tree[0][1])
        tree.pop(0)
    print("Huffman Coding: ")
    for i in code:
        print(i, "=>", code[i])

if __name__ == '__main__':
    message = get_seq()
    print(message)
    count = {}
    for c in message:
        if c not in count:
            count[c] = 1
        else:
            count[c] += 1
    #print(count)
    for c in sorted(count):
        print(c, "=>", count[c]/len(message))
    print("Count of different symblos(alphabet): ", len(count))
    print("Entropy value: ", Entropy_value(count, len(message)))
    print("Shannon-Fano Coding: ")
    Shannon_Fano_coding(count, "")
    Huffman_coding(count)