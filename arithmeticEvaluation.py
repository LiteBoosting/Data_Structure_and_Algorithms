# -*- coding: utf-8 -*-
from copy import deepcopy

a = 's'
a in ('a', 's', 'd', 'f')

#%%
class arithmetic(object):
    """Return evaluation of a given arithmetic expression (stored as a string).
    As version-1, this solver has the following contraints:
    1. Only numbers(int or float), 4 basic operators (+, -, *, /), and left/right
       parenthesis are effective elements.
    2. There should be a seperator (single space) between each effective element in the string.
    3. There is no conderation of operation priority among '+', '-' and '*', '/', i.e.,
       every operation of two numbers should be embraced by a pair of parenthesis.
    4. This is an implementation of the so-called two-stack algorithm.
       1. Value: push onto the value stack.
       2. Operator: push onto the operator stack.
       3. Left parenthesis: ignore.
       4. Right parenthesis: pop operator and two values;
       5. Push the result of applying that operator to those values onto the operand stack.
    """
    
    def __init__(self, expression):
        self.expression = expression.split(' ')
        self.valueStack = []
        self.operatorStack = []

    def elementType(self, element):
        """Return the type of element.
        value, operator, leftParenthesis, rightParenthesis.
        Current version is simple, they should be improved.
        """
        if element == '(':
            return 'leftParenthesis'
        elif element == ')':
            return 'rightParenthesis'
        elif element in ('+', '-', '*', '/'):
            return 'operator'
        else:
            return 'value'
            
    def bi_operation(self, value1, value2, operator):
        """Return value of the operation on the two values.
        """
        if operator == '+':
            return float(value1) + float(value2)
        elif operator == '-':
            return float(value1) - float(value2)
        elif operator == '*':
            return float(value1) * float(value2)
        elif operator == '/':
            return float(value1) / float(value2)
            
    def evaluation(self):
        for element in self.expression:
            if self.elementType(element) == 'leftParenthesis':
                continue
            elif self.elementType(element) == 'value':
                self.valueStack.append(element)
            elif self.elementType(element) == 'operator':
                self.operatorStack.append(element)
            elif self.elementType(element) == 'rightParenthesis':
                result = self.bi_operation(self.valueStack.pop(), self.valueStack.pop(), self.operatorStack.pop())
                self.valueStack.append(result)
        return self.valueStack.pop()
#%%
e_obj = '( ( 1 + 2 ) + 3 )'
a_obj = arithmetic(e_obj)
print a_obj.evaluation()
print a_obj.expression
print a_obj.operatorStack
print a_obj.valueStack            
