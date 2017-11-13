#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
class Node(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BST(object):
    def __init__(self, root):
        self.root = root
        
    def put(self, key, value, node='Root'):
        if value == None:
            return self.delete(key)
        if node == 'Root':
            node_temp = self.root
        else:
            node_temp = node
        if key == node_temp.key:
            node_temp.value = value
            return None
        elif key > node_temp.key:
            if node_temp.right == None:
                node_temp.right = Node(key, value)
            else:
                node_temp = node_temp.right
                return self.put(key, value, node=node_temp)
        elif key < node_temp.key:
            if node_temp.left == None:
                node_temp.left = Node(key, value)
            else:
                node_temp = node_temp.left
                return self.put(key, value, node=node_temp)
        else:
            return "Value for key is not comparable"
        
    def get(self, key, node='Root'):
        if node == 'Root':
            node_temp = self.root
        else:
            node_temp = node
        if key == node_temp.key:
            return node_temp.value
        elif key > node_temp.key:
            if node_temp.right == None:
                return "Not found"
            else:
                node_temp = node_temp.right
                return self.get(key, node=node_temp)
        elif key < node_temp.key:
            if node_temp.left == None:
                return "Not found"
            else:
                node_temp = node_temp.left
                return self.get(key, node=node_temp)
        else:
            return "Value for key is not comparable"

#%%
key_list = [1, 2, 5, 0, 0.2]
value_list = [0, 1, 2, 3, 4]

for i, (key, value) in enumerate(zip(key_list, value_list)):
    node = Node(key, value)
    if i == 0:
        BST_1 = BST(node)
    else:
        BST_1.put(key, value)

print(BST_1.get(2))
print(BST_1.get(5))
print(BST_1.get(1))
print(BST_1.get(0))
print(BST_1.get(0.2))
print(BST_1.get(0.23))

#%%
# Generate random number
import numpy as np
n = 100000
key_list = np.random.normal(loc=0.0, scale=1.0, size=n)
value_list = np.random.normal(loc=0.0, scale=1.0, size=n)+np.full((n,), 100)

for i, (key, value) in enumerate(zip(key_list, value_list)):
    if i == 0:
        BST_2 = BST(Node(key, value))
    else:
        BST_2.put(key, value)

print(BST_2.get(key_list[0]), value_list[0])
print(BST_2.get(key_list[1000]), value_list[1000])
print(BST_2.get(key_list[20000]), value_list[20000])
print(BST_2.get(key_list[30000]), value_list[30000])
print(BST_2.get(key_list[40000]), value_list[40000])
print(BST_2.get(0.23))
