import sys
import hashlib
import numpy as np

noLines = 0
lines = []
noQ = 0
q=[]
hashes = {}
hashList = []

def readInput():
    global lines, noLines, noQ, q, hashList
    i = 1
    for line in sys.stdin:
        if i == 1:
            noLines = int(line.rstrip())
        elif i <= noLines + 1:
            hashList.append(simhash(line.rstrip()))
        elif i == noLines + 2:
            noQ = int(line.rstrip())
        elif i <= noLines + 2 + noQ:
            q.append(line.rstrip())
        i += 1


def simhash(input):
    global hashes
    individuals = input.split(" ")
    sh = np.zeros(128, dtype=np.int64)
    for ind in individuals:
        a = 1
        temp = hashes.get(ind, None)
        if temp is not None:
            sh -= 1 - temp
            sh += temp
            continue

        hash = hashlib.md5(ind.encode('utf-8')).hexdigest()
        hashBits = format(int(hash, 16), '0>128b')
        hashBits = np.array(list(map(int, list(hashBits))), dtype=np.int64)
        hashes[ind] = hashBits
        sh -= 1 - hashBits
        sh += hashBits
    sh[sh >= 0] = 1
    sh[sh < 0] = 0
    temp = ''.join([str(s) for s in sh])
    return temp


def runQueries(candidates):
    global hashList
    printlist = []
    for query in q:
        textIndex = int(query.split(" ")[0])
        diff = int(query.split(" ")[1])

        similar = candidates[textIndex]
        text = hashList[textIndex]
        printVal = 0
        for ind in set(similar):
            hash = hashList[ind]
            differences = 0
            for a, b in zip(hash, text):
                if a != b:
                    differences+=1
                    if differences > diff:
                        break
            if differences <= diff:
                printVal += 1
        printlist.append(printVal)
    print(*printlist, sep='\n', end="")


def lsh():
    candidates = {curr_id: list() for curr_id in range(noLines)}
    for pojas in range(1, 9):
        pretinci = {}
        for curr_id in range(noLines):
            hash = hashList[curr_id]
            #Sad uzmi samo 16 bitova koji pripadaju tom pojasu
            val = int(hash[(pojas - 1) * 16: pojas * 16], 2)
            texts_in_shell = set()
            if pretinci.get(val, None) is not None:
                texts_in_shell = pretinci[val]
                for text_id in texts_in_shell:
                    candidates[curr_id].append(text_id)
                    if candidates.get(text_id, None) is None:
                        candidates[text_id] = []
                    candidates[text_id].append(curr_id)
            else:
                texts_in_shell = set()

            texts_in_shell.add(curr_id)
            pretinci[val] = texts_in_shell.copy()
    return candidates

if __name__ == '__main__':
    readInput()
    candidates = lsh()
    runQueries(candidates)