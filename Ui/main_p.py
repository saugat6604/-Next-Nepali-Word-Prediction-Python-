vo={
    'a':'',
    'aa':'ा',
    'i':'ि',
    'ee':'ी',
    'u':'ु',
    'oo':'ू',
    'e':'े',
    'ai':'ै',
    'o':'ो',
    'au':'ौ'
}

voa={
    'a':'अ',
    'aa':'आ',
    'i':'इ',
    'ee':'ई',
    'u':'उ',
    'oo':'ऊ',
    'e':'ए',
    'ai':'ऐ',
    'o':'ओ',
    'au':'औ'
}


co1 ={
    'k':'क',
    'g':'ग',
    'x':'छ',
    'j':'ज',
    'z':'ज',
    'p':'प',
    'f':'फ',
    
    'v':'भ',
    'm':'म',
    'y':'य',
    'r':'र',
    'l':'ल',
    'w':'व',
    'h':'ह',
    
}

co2 = {
    'kh':'ख',
    'gh':'घ',
    'ch':'च',
    'jh':'झ',
    'ph':'फ',
    'bh':'भ',
    'sh':'श'
}

co3={
    'chh':'छ',
    'ksh':'क्ष',
    'gny':'ज्ञ'
}

coar={
    'b':['ब','व'],
    's':['स','श','ष'],
    't':['ट','त'],
    'th':['ठ','थ'],
    'd':['ड','द'],
    'dh':['ढ','ध'],
    'n':['न','ङ','ञ','ण']
}


def suggest(inp):
    # returns first element of array and 
    # whole possible array of suggestion for given input text.
    inp=inp.lower()
    result=""
    first=0
    resultar=[]
    index=0
    while True:
        chunk3 = inp[:3] if len(inp)>2 else ''
        chunk2= inp[:2] if len(inp)>1 else ''
        chunk1=inp[:1]
        if not chunk1: break
        is_vowel=False
        if chunk3 in co3:
            result+=co3[chunk3]
            size=3
            pass
        elif chunk2 in co2:
            result+=co2[chunk2]
            size=2
            pass
        elif chunk1 in co1:
            result+=co1[chunk1]
            size=1
            pass
        elif chunk2 in coar:
            aray=coar[chunk2]
            tempar=[]
            newindex=len(result)
            if resultar:
                for i in resultar:
                    for j in aray:
                        tempar.append(i+result[index:newindex]+j)
                resultar=tempar[:]
            else:
                resultar=[result+i for i in aray]
            index=len(resultar[0])
            result=resultar[0]
            size=2
            pass
        elif chunk1 in coar:
            aray=coar[chunk1]
            tempar=[]
            newindex=len(result)
            if resultar:
                for i in resultar:
                    for j in aray:
                        tempar.append(i+result[index:newindex]+j)
                resultar=tempar[:]
            elif chunk1=='n' and not result:
                first=1
            else:
                resultar=[result+i for i in aray]
            if first:
                result='न'
                first=0
            else:
                index=len(resultar[0])
                result=resultar[0]
            size=1
            pass
        elif chunk2 in voa:
            is_vowel=True
            result+=voa[chunk2]
            size=2
            pass
        elif chunk1 in voa:
            is_vowel=True
            result+=voa[chunk1]
            size=1
            pass
        else:
            print("X")
            size=len(inp)

        inp=inp[size:]
        chunk2= inp[:2] if len(inp)>1 else ''
        chunk1=inp[:1]
        size=0
        if not chunk1: break

        if chunk2 in vo:
            result+=vo[chunk2]
            size = 2
            pass
        elif chunk1 in vo:
            result+=vo[chunk1]
            size = 1
            pass
        else:
            if is_vowel:
                pass
            else:
                result+='्'
        inp=inp[size:]
    
    newindex=len(result)
    if resultar and index!=newindex:
        for i in range(len(resultar)):
            resultar[i]+=result[index:newindex]
    return result,resultar


print(suggest("kalam"))

import json


with open('map.json') as mp:
    mapping = json.load(mp)

import re
d={
    'aa':'a',
    'z':'j',
    'sh':'s',
    'f':'ph',
    'v':'bh',
    'ee':'i',
    'oo':'u',
    'w':'b'
}
def funconvert(s):
    # map aa -> a,    f->ph
    v=[(m.start(0), m.end(0)) for m in re.finditer('(aa)|z|w|sh|f|v|(oo)|(ee)', s)]
    if not v: return s
    l=s[:]
    for j in v:
        key=s[j[0]:j[1]]
        l=l.replace(key,d[key],1)
    return l

def newfun(text):
    # prints using static rule and mapping results from map.json
    for i in text.split():
        print(suggest(i),end="\t")
        h=funconvert(i)
        print(mapping.get(h,'None'))
        

