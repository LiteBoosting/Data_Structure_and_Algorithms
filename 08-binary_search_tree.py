#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
from collections import deque

#%%
class TreeNode(object):
    def __init__(self, key, value, leftChild=None, rightChild=None, parent=None):
        self.key = key
        self.value = value
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.parent = parent
    
    def hasLeftChild(self):
        return (self.leftChild is not None)
    
    def hasRightChild(self):
        return (self.rightChild is not None)
    
    def isLeftChild(self):
        return ((self.parent is not None) and (self.parent.leftChild is self))
    
    def isRightChild(self):
        return ((self.parent is not None) and (self.parent.rightChild is self))
    
    def isRoot(self):
        return (self.parent is None)
    
    def isLeaf(self): # Root, Branch, and Leaf
        return ((self.leftChild is None) and (self.rightChild is None))
    
    def hasAnyChildren(self):
        return ((self.leftChild is not None) or (self.rightChild is not None))
    
    def hasBothChildren(self):
        return ((self.leftChild is not None) and (self.rightChild is not None))
    
#%%
class BinarySearchTree(object):
    def __init__(self):
        self.root = None
        self.size = 0
    
    def put(self, key, value):
        if self.root is None:
            if value is not None:
                self.root = TreeNode(key, value)
                self.size += 1
            else:
                return None
        else:
            return self._put(key, value)

    def _put(self, key, value, currentNode='root'):
        if value == None:
            return self.delete(key)
        if currentNode == 'root':
            currentNode = self.root
        try:
            if key == currentNode.key:
                currentNode.value = value
                self.size += 1
                return None
            elif key > currentNode.key:
                if currentNode.hasRightChild():
                    currentNode = currentNode.rightChild
                    return self._put(key, value, currentNode=currentNode)
                else:
                    currentNode.rightChild = TreeNode(key, value, parent=currentNode)
                    self.size += 1
                    return
            elif key < currentNode.key:
                if currentNode.hasLeftChild():
                    currentNode = currentNode.leftChild
                    return self._put(key, value, currentNode=currentNode)
                else:
                    currentNode.leftChild = TreeNode(key, value, parent=currentNode)
                    self.size += 1
                    return
        except:
            raise ValueError("The key must be comparable - ", key, currentNode.key)
        
    def get(self, key):
        if self.root is None:
            return None
        else:
            returnNode = self._get(key)
            if returnNode is None:
                return None
            else:
                return returnNode.value
    
    def _get(self, key, currentNode='root'):
        '''The whole node is returned instead of the value.
           The reason is that we want to use this function for self._delete() as well.
        '''
        if currentNode == 'root':
            currentNode = self.root
        try:
            if key == currentNode.key:
                return currentNode
            elif key > currentNode.key:
                if currentNode.hasRightChild():
                    currentNode = currentNode.rightChild
                    return self._get(key, currentNode=currentNode)
                else:
                    return None
            else: # key < currentNode.key:
                if currentNode.hasLeftChild():
                    currentNode = currentNode.leftChild
                    return self._get(key, currentNode=currentNode)
                else:
                    return None
        except:
            raise ValueError("The key must be comparable - ", key, currentNode.key)

    def delete(self, key):
        if self.root is None:
            return
        else:
            return self._delete(key)
    
    def _delete(self, key):
        try:
            foundNode = self._get(key)
            if foundNode is not None:
                while True:
                    if foundNode.isLeaf():
                        self._deleteLeafNode(foundNode)
                        return
                    elif foundNode.hasBothChildren():
                        successorNode = self._getSuccessorNode(foundNode)
                        foundNode.key = successorNode.key
                        foundNode.value = successorNode.value
                        if successorNode.isLeaf():
                            self._deleteLeafNode(successorNode)
                        else: # successorNode has single child
                            self._deleteSingleChildNode(successorNode)
                        return
                    else: # foundNode has single child
                        self._deleteSingleChildNode(foundNode)
                        return
            else:
                return "Key not found"
        except:
            raise ValueError("The key must be comparable - ", key, self.root.key)
        
    def _deleteLeafNode(self, node):
        if node.hasAnyChildren():
            raise ValueError("Node having at least one children passed to _deleteLeafNode().")
        if node.isRoot():
            self.root = None
            self.size -= 1
            return
        if node.isLeftChild():
            node.parent.leftChild = None
        else: # node.isRightChild():
            node.parent.rightChild = None
        self.size -= 1
        return
    
    def _deleteSingleChildNode(self, node):
        if node.hasBothChildren():
            raise ValueError("Node having both children passed to _deleteSingleChildNode().")
        if node.isLeaf():
            raise ValueError("Leaf node passed to _deleteSingleChildNode().")
        if node.isRoot():
            if node.hasLeftChild():
                self.root = node.leftChild
                node.leftChild.parent = None
            else: # node.hasRightChild():
                self.root = node.rightChild
                node.rightChild.parent = None
            self.size -= 1
            return
        if node.hasLeftChild():
            if node.isLeftChild():
                node.parent.leftChild = node.leftChild
                node.leftChild.parent = node.parent
            else: # node.isRightChild():
                node.parent.rightChild = node.leftChild
                node.leftChild.parent = node.parent
        else: # node.hasRightChild():
            if node.isLeftChild():
                node.parent.leftChild = node.rightChild
                node.rightChild.parent = node.parent
            else: # node.isRightChild():
                node.parent.rightChild = node.rightChild
                node.rightChild.parent = node.parent
        self.size -= 1
        return

    def _getSuccessorNode(self, node):
        '''The node returned is actually left succesor.
        '''
        if not node.hasBothChildren():
            raise ValueError("Node not having both children passed to _getSuccessorNode().")
        successorNode = node.leftChild
        while successorNode.hasRightChild():
            successorNode = successorNode.rightChild
        return successorNode
    
    def orderedTraverse(self):
        self.ordered_key_list = []
        self._orderedTraverse2()
        return self.ordered_key_list
    
    def _orderedTraverse(self, node=None):
        if node is None:
            return
        self._orderedTraverse(node.leftChild)
        self.ordered_key_list.append(node.key)
        self._orderedTraverse(node.rightChild)
        return
    
    def _orderedTraverse2(self):
        operation_stack = []
        operation_stack.append(self.root)
        self.popedLeftChild = False
        while len(operation_stack) > 0:
            node = operation_stack.pop()
            if node == '+':
                node = operation_stack.pop()
                self.popedLeftChild = True
            if node.isLeaf(): # pop the node and delete the node
                self.ordered_key_list.append(node.key)
            elif (node.hasLeftChild()) and (not self.popedLeftChild): # append the node and its leftChild
                operation_stack.extend([node, '+', node.leftChild])
            else:  # only has right child, pop the node, delete the node, and append its rightChild
                self.ordered_key_list.append(node.key)
                operation_stack.append(node.rightChild)
        return
    
    def depthFirstTraverse(self):
        self.depthFirstTraverse_list = []
        self.depthFirstTraverse_key_list = []
        operation_stack = []
        operation_stack.append(self.root)
        while operation_stack:
            node = operation_stack.pop()
            self.depthFirstTraverse_list.append(node)
            self.depthFirstTraverse_key_list.append(node.key)
            if node.hasRightChild():
                operation_stack.append(node.rightChild)
            if node.hasLeftChild():
                operation_stack.append(node.leftChild)
        return self.depthFirstTraverse_key_list

    def breadthFirstTraverse(self):
        self.breadthFirstTraverse_list = []
        self.breadthFirstTraverse_key_list = []
        operation_queue = deque()
        operation_queue.append(self.root)
        while operation_queue:
            node = operation_queue.popleft()
            self.breadthFirstTraverse_list.append(node)
            self.breadthFirstTraverse_key_list.append(node.key)
            if node.hasLeftChild():
                operation_queue.append(node.leftChild)
            if node.hasRightChild():
                operation_queue.append(node.rightChild)
        return self.breadthFirstTraverse_key_list
    
#%%
def printNode(node):
    if node is not None:
        print('key:', node.key, ', value:', node.value)
    else:
        print('None')

#%%
key_list   = [1.0, 2.0, 5.0, 0.0, 0.2, 'x', 'y', 0.9, 0.1]
value_list = ['a', 'b', '2', '3', '4', 'a', 'c', 1.9, 1.8]

BST_1 = BinarySearchTree()

for key, value in zip(key_list, value_list):
    try:
        BST_1.put(key, value)
    except:
        print("Not able to insert - ", (key, value))

#%%
BST_1.orderedTraverse()

#%%
BST_1.depthFirstTraverse()

#%%
BST_1.breadthFirstTraverse()

#%%
printNode(BST_1.root)

printNode(BST_1.root.leftChild)
printNode(BST_1.root.leftChild.rightChild)
printNode(BST_1.root.leftChild.rightChild.rightChild)

printNode(BST_1.root.rightChild)
printNode(BST_1.root.rightChild.rightChild)

#%%
for key in key_list:
    try:
        print(BST_1.get(key))
    except:
        print("The key is not comparable")

print(BST_1.get('aaa'))

#%%
BST_1.delete(0.0)
printNode(BST_1.root)

printNode(BST_1.root.leftChild)
printNode(BST_1.root.leftChild.rightChild)
print(BST_1.root.leftChild.rightChild.hasRightChild())

printNode(BST_1.root.rightChild)
printNode(BST_1.root.rightChild.rightChild)

#%%
for key in [0.2, 0.9, 2.0, 5.0]:
    BST_1.delete(key)
printNode(BST_1.root)
print(BST_1.root.isLeaf())

#%%
printNode(BST_1.root.rightChild)
printNode(BST_1.root.leftChild)

#%%
import numpy as np
n = 100
value_baseline = 100
key_list = np.random.normal(loc=0.0, scale=1.0, size=n)
value_list = np.random.normal(loc=0.0, scale=1.0, size=n)+np.full((n,), value_baseline)
BST_2 = BinarySearchTree()
print(BST_2.size)
for key, value in zip(key_list, value_list):
    BST_2.put(key, value)
print(BST_2.size)

#%%
for m in [0, min(10, n-1), min(100, n-1)]:
    print(BST_2.get(key_list[m]), value_list[m])

print(BST_2.get(0.23))
print(BST_2.get('0.23'))

#%%
while not BST_2.root.isLeaf():
    BST_2.delete(BST_2.root.key)
print(BST_2.size)
