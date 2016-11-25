from __future__ import print_function
from PIL import Image
from numpy.lib.scimath import log2
from operator import itemgetter
import math
Shannon_Fano_dict={}
Huffman_dict = {}
equable_dict ={}
def get_seq():
    #Image.open("temp.jpg").convert("L").save("tes.jpg")
    image = Image.open("test.jpg")#загружаем енотиков
    print(image.format, image.size, image.mode)#Проверяем формат
    width = image.size[0] #Определяем ширину.
    height = image.size[1] #Определяем высоту.
    source = image.load() #Выгружаем пиксели
    message = [] #Список для элементов
    for i in range (width):
         message.append(round(float(source[i, height/2-1])/20)*20)
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
        Shannon_Fano_dict[seq.popitem()[0]] = code
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
    for i in code:
        Huffman_dict[i] = code[i]

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

    #Alphabet
    print("Count of different symblos(alphabet): ", len(count))

    #Entropy
    print("Entropy value: ", Entropy_value(count, len(message)))

    #Equal Code
    print("Equal code: ")
    med = math.ceil(log2(len(count)))
    print("Code length : ", med)
    equable_dict = dict.fromkeys(count, "")
    code = 0
    for i in equable_dict:
        equable_dict[i] =bin(code)
        equable_dict[i] = equable_dict[i][2:len(equable_dict[i]):1]
        while len(equable_dict[i]) != med:
            equable_dict[i] = "0" + equable_dict[i]
        code += 1
    for i in sorted(equable_dict):
        print(i, "=", equable_dict[i])
    code_mes = ""
    for i in message:
        code_mes += equable_dict[i]
    print("Message length in code: ", len(code_mes), "\nMessage code: ", code_mes)

    #Shannon-Fano Code
    print("Shannon-Fano Coding: ")
    Shannon_Fano_coding(count, "")
    for i in sorted(Shannon_Fano_dict):
        print(i, "=", Shannon_Fano_dict[i])
    code_mes = ""
    for i in message:
        code_mes += Shannon_Fano_dict[i]
    print("Message length in code: ", len(code_mes), "\nMessage code: ", code_mes)

    #Huffman code
    Huffman_coding(count)
    for i in sorted(Huffman_dict):
        print(i, "=", Huffman_dict[i])
    code_mes = ""
    for i in message:
        code_mes += Huffman_dict[i]
    print("Message length in code: ", len(code_mes), "\nMessage code: ", code_mes)
