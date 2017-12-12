#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np

#%%
class PMTableBuild(object):
    '''PMTable is the partial match table, defined as: given i matches and (i+1)-th being unmatched
    (i from 0 to self.len-1), PMT[i] is the length of the longest possible suffix substring ending at the
    last matched char (string[i-1], position starts at 0) which is also a prefix substring.
    Value '-1' is allowed for PMT when even the unmatched one can not be a prefix substring.
    
    See Github Wiki for another explanation (this explanation is more useful when we do string search).
    
    Version 0 is that we use brutal force way to build this table, its complexity is k-squared,
    where k is length of the string.
    
    Version 1 uses a smart way to build the table (essentially same idea as the KMP algorithm), and the
    complexity reduces to k.
    
    When we do substring match, the matched part is matchedSubstr, the unmatched part (single character,
    since we stop the match once unmacthed) is unmatchedChar. They can be denoted as MtStr and UnChar
    for short.
    '''
    def __init__(self, string):
        self.string = string
        self.len = len(string)
        self.PMT = np.full((self.len,), -1, dtype=int)
    
    def PMTableBuild_v0(self):
        for i in range(1, self.len):
            for j in range(i-1, -1, -1):
                if all(self.match(self.string[(i-j):i], self.string[i])):
                    self.PMT[i] = j
                    break
    
    def match(self, MtStr, UnChar):
        match_MtStr = True
        match_UnChar = True
        for i in range(len(MtStr)):
            if MtStr[i] != self.string[i]:
                match_MtStr = False
                break
        if UnChar == self.string[len(MtStr)]:
            match_UnChar = False
        return (match_MtStr, match_UnChar)
    
    def PMTableBuild_v1(self):
        self.PMT_MtStr = np.full((self.len,), None) # dtype=int
        self.PMT[0] = -1
        self.PMT_MtStr[0] = 0
        for i in range(1, self.len): # i is last matched location
            for j in range(self.PMT_MtStr[i-1]+1, -1, -1): # j is length of substring to match prefix
                match_MtStr, match_UnChar = self.match(self.string[(i-j):i], self.string[i])
                if match_MtStr:
                    if not self.PMT_MtStr[i]:
                        self.PMT_MtStr[i] = j
                    if match_UnChar:
                        self.PMT[i] = j
                        break

#%%
string = 'ABCDABD'
string = 'ABCDABCDABD'
PMT_A = PMTableBuild(string)
PMT_A.PMTableBuild_v0()
print(PMT_A.PMT)

PMT_B = PMTableBuild(string)
PMT_B.PMTableBuild_v1()
print(PMT_B.PMT)

#%%
class KMPStringSearch(object):
    def __init__(self, string, text, PMT):
        self.string = string
        self.text = text
        self.len = len(self.string)
        self.size = len(self.text)
        self.PMT = PMT
        self.num_comparisons = 0
        self.isMatchedKMP, self.locKMP = self.KMPStringSearch_v0()
        print("self.num_comparisons", self.num_comparisons)
        self.num_comparisons = 0
        self.isMatchedBF, self.locBF = self.BrutalForceStringSearch_v0()
        print("self.num_comparisons", self.num_comparisons)
    
    def BrutalForceStringSearch_v0(self):
        i = 0
        j = 0
        while i+self.len < self.size:
            isMatched, matches = self.stringMatch(textLoc=i, stringLoc=j)
            if isMatched:
                return (isMatched, i)
            else:
                i += 1
        return (False, None)

    def KMPStringSearch_v0(self):
        i = 0
        j = 0
        while i+self.len < self.size:
            isMatched, matches = self.stringMatch(textLoc=i, stringLoc=j)
            if isMatched:
                return (isMatched, i)
            else:
                i += matches - self.PMT[matches]
                j = max(0, self.PMT[matches])
        return (False, None)
    
    def stringMatch(self, textLoc, stringLoc=0):
        '''Given location i of the text, return matched, and number of matches.
        '''
        i = textLoc
        j = stringLoc
        while j < self.len:
            if self.compare(self.string[j], self.text[i]):
                i += 1
                j += 1
            else:
                return (False, max(0, j-1))
        return (True, max(0, j-1))
    
    def compare(self, char0, char1):
        self.num_comparisons += 1
        return char0 == char1

#%%
text = '''
PMTable is partial match table, which is defined as given i matches and (i+1)-th being not matched
    (i from 0 to self.len-1), PMT[i] is the length of the longest possible suffix substring ending at the
    lst matched char (string[i-1], position starts at 0) which is also a prefix substring.
    Value '-1' is allowed for PMT when even the unmatched one can not be a prefix substring. is is is is i
    is lengtth
    This is version-0, in which we use brutal force way to build this table, its complexity is k-squared,
    where k is length of the string.
'''
string = 'is length '
PMT_array = PMTableBuild(string).PMT
KMPStringSearch_obj = KMPStringSearch(string, text, PMT_array)
print(KMPStringSearch_obj.isMatchedKMP, KMPStringSearch_obj.locKMP)
print(KMPStringSearch_obj.isMatchedBF, KMPStringSearch_obj.locBF)

#%%
text = 'a'*100+'b'
string = 'a'*10+'b'
PMT_array = PMTableBuild(string).PMT
KMPStringSearch_obj = KMPStringSearch(string, text, PMT_array)
print(KMPStringSearch_obj.isMatchedKMP, KMPStringSearch_obj.locKMP)
print(KMPStringSearch_obj.isMatchedBF, KMPStringSearch_obj.locBF)

