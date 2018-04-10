import math
import random
import time

"""
Implemented the Markov chain with dictionaries, sympy was too much
overhead apparently
"""

class MarkovText:

    def __init__(self, trainingFile):
        tick = time.clock()
        
        self.trainingFile = trainingFile
        self.matrix = dict()
        inFile = open(trainingFile,"r")
        previousWord = ""
        linesParsed = 0
        while True:
            buffer = inFile.readline()
            if not buffer:
                break
            previousWord = self.train(buffer.split(), previousWord)
            linesParsed += 1
        tock = time.clock()
        print("Parsed",linesParsed,"lines in",tock - tick,"seconds")
            
    def addEntry(self, word):
        if word in self.matrix:
            return
        self.matrix[word] = Entry()

    def connect(self, word1, word2):
        self.matrix[word1].addEdge(word2)

    def train(self, data, previous = ""):
        
        for word in data:
            word = word.lower()
            self.addEntry(word)
            
            if previous != "":
                self.connect(previous, word)

            previous = word
        return previous

    def getSuccessor(self, seedWord):
        if seedWord in self.matrix:
            return self.matrix[seedWord].probableSuccessor()
        return ""

    def generate(self, numWords, word):
        soFar = []
        
        while numWords and word:
            soFar += [word]
            word = self.getSuccessor(word)
            numWords -= 1
        return soFar

class Entry:
    def __init__(self):
        self.row = dict()
        self.counts = 0

    def addEdge(self, word):
        if word in self.row:
            self.row[word] += 1
        else:
            self.row[word] = 1
        self.counts += 1

    def probableSuccessor(self):
        if self.counts == 0:
            return ""
        
        keys = list(self.row.keys())
        vals = list(self.row.values())
        return pickByProb(keys, [val * 1.0 / self.counts for val in vals])

def pickByProb(elems, probs):
    assert(len(elems) == len(probs))
    p = random.random()
    for elem, prob in zip(elems, probs):
        
        p -= prob
        if p <= 0:
            
            return elem

def generate(file, numWords, keyWord, filterOutFN = lambda x: False):
    m = MarkovText(file)
    i = 0
    buffer = ""
    for word in m.generate(numWords, keyWord):
        if not filterOutFN(word):
            buffer += word + " "
    return buffer

