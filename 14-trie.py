#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import string

#%%
#==============================================================================
# 1. Only use pure small case English letters
# 2. You come up with some words from copying certain context
# 3. assign them random values
# 4. define insert, get(), and delete()
#==============================================================================
text = ['here you can get help of any object by pressing command plus i in front of it either',
        'on the editor or the console help can also be shown automatically after writing a left',
        'parenthesis next to an object you can activate this behavior in preferences then help']

#%%
class trieNode(object):
    def __init__(self, value):
        self.value = value
        self.next = {}

#%%
class trieTree(object):
    def __init__(self, charSet):
        self.charSet = charSet
        self.root = trieNode(value=None)
    
    def insert(self, string, value):
        tempNode = self.root
        for digit, char in enumerate(string):
            if tempNode.next.get(char, None):
                tempNode = tempNode.next[char]
            else:
                tempNode.next[char] = trieNode(value=None)
                tempNode = tempNode.next[char]
        tempNode.value = value
    
    def get(self, string):
        node = self.getNode(string)
        if not node:
            return None
        else:
            return node.value
    
    def getNode(self, string):
        tempNode = self.root
        for digit, char in enumerate(string):
            if tempNode.next.get(char, None):
                tempNode = tempNode.next[char]
            else:
                return None
        return tempNode
    
    def isLeaf(self, node):
        return not node.next.keys()
    
    def delete(self, string):
        tempNode = self.root
        record = []
        record.append(tempNode)
        for digit, char in enumerate(string):
            if tempNode.next.get(char, None):
                tempNode = tempNode.next[char]
                record.append(tempNode)
            else:
                return "not found"
        for i in range(len(record)-1, 0, -1):
            j = i-1
            char = string[j]
            record[i].value = None
            if self.isLeaf(record[i]):
                record[j].next.pop(char, None)

#%%
separatedText = [word for x in text for word in x.split(' ')]
charSet = list(string.ascii_lowercase)
trieDict = trieTree(charSet)
for i, word in enumerate(separatedText):
    trieDict.insert(word, i)
for i, word in enumerate(separatedText):
    print(word, trieDict.get(word))
print('here', trieDict.get('here'))
trieDict.delete('here')
print('here', trieDict.get('here'))
