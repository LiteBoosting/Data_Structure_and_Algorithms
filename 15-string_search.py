#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import numpy as np

#%%
class PMTableBuild(object):
    '''PMTable is partial match table, which is defined as given i matches and (i+1)-th being not matched
    (i from 0 to self.len-1), PMT[i] is the length of the longest possible suffix substring ending at the
    lst matched char (string[i-1], position starts at 0) which is also a prefix substring.
    Value '-1' is allowed for PMT when even the unmatched one can not be a prefix substring.
    This is version-0, in which we use brutal force way to build this table, its complexity is k-squared,
    where k is length of the string.
    '''
    def __init__(self, string):
        self.string = string
        self.len = len(string)
        self.PMT = np.full((self.len,), -1, dtype=int)
        self.PMTableBuild_v0()
    
    def PMTableBuild_v0(self):
        for i in range(1, self.len):
            for j in range(i-1, -1, -1):
                if self.match(self.string[(i-j):i], self.string[i]):
                    self.PMT[i] = j
                    break
    
    def match(self, matchedSubstr, unmatchedChar):
        for i in range(len(matchedSubstr)):
            if matchedSubstr[i] != self.string[i]:
                return False
        if unmatchedChar == self.string[len(matchedSubstr)]:
            return False
        return True

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
