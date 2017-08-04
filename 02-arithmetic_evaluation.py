# -*- coding: utf-8 -*-
from copy import deepcopy

#%%
class arithmetic(object):
    """Return evaluation of a given arithmetic expression (stored as a string).
    As version-2, this solver has less contraints than version-1:
    1. Only numbers(int or float), 4 basic operators (+, -, *, /), and left/right
       parentheses are effective elements. (still true)
    2. There should be a seperator (single space) between each effective element in the string. (false,
       intelligent parsing has been implemented)
    3. There is no consideration of operation priority among '+', '-' and '*', '/', i.e.,
       every operation of two numbers should be embraced by a pair of parentheses. (false, priority has
       been considered in a proper way)
    4. This is an implementation of the so-called two-stack algorithm: (false, new algorithm is applied)
        1. Value: push onto the value stack.
        2. Operator: push onto the operator stack.
        3. Left parenthesis: ignore.
        4. Right parenthesis: pop operator and two values;
        5. Push the result of applying that operator to those values onto the operand stack.
    5. The algorithm contains following steps:
        1. Values, operators and parentheses are in the same stack.
        2. Whenever we meet right parenthesis, pop out elements until we pop one and exactly one left
           parenthesis.
        3. Apply the no_parenthesis_evaluation on poped elements.
        4. When we touch the end of the list, implement the no_parenthesis_evaluation on whole list.
        5. no_parenthesis_evaluation: go through operators in the sub_list, if see either * or /, then
           go through until we see a + or -, or touch the end of sub_list, then pop this segment out and
           implement a sequential evaluation, return the value to the sub_stack and go on to find next
           prioritied segment (continuous * or /). When we touched the end of sub_list, implement the
           sequential evaluation on the whole sub_list.
    """
    
    def __init__(self, expression, verbose=False):
        self.raw_expression = expression
        self.valueStack = []
        self.operatorStack = []
        self.verbose = verbose

    def parser(self):
        self.expression = []
        value_record = ''
        for char in self.raw_expression + ' ':
            if char in ('(', ')', '+', '-', '*', '/'):
                if value_record != '':
                    self.expression.append(value_record)
                    value_record = ''
                self.expression.append(char)
            elif char in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'):
                value_record += char
            else:
                if value_record != '':
                    self.expression.append(value_record)
                    value_record = ''
                continue
            
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
            
    def bi_evaluation(self, value1, value2, operator):
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
            
    def sequential_evaluation(self, sub_list):
        seq_list = deepcopy(list(reversed(sub_list)))
        if len(seq_list) == 1:
            if self.elementType(seq_list[0]) == 'value':
                return seq_list[0]
            else:
                raise ValueError('value error:' + '(' + seq_list[0] + ')')
        while len(seq_list) > 1:
            if self.verbose:
                print "seq_list:", list(reversed(seq_list))
            value1 = seq_list.pop()
            operator = seq_list.pop()
            value2 = seq_list.pop()
            seq_list.append(self.bi_evaluation(value1, value2, operator))
        return seq_list[0]
                
    def no_parenthesis_evaluation(self, sub_list):
        """Evaluate an expression without any parenthesis.
        Every time we meet a right parenthesis, we pop things out until we see a left parenthesis.
        Therefore we need a no-parenthesis expression evaluation.
        """
        np_list = deepcopy(sub_list) # np_list means no parenthesis list
        if len(np_list) == 1:
            if self.elementType(np_list[0]) == 'value':
                return np_list[0]
            else:
                raise ValueError('value error:' + '(' + np_list[0] + ')')
        np_list.append('end')
        running_list = []
        seq_list = []
        switch_key = 'off'
        for element in np_list:
            if element in ('*', '/'):
                if switch_key == 'off':
                    switch_key = 'on'
                    seq_list.append(running_list.pop())
                seq_list.append(element)
            elif element in ('+', '-'):
                if switch_key == 'on':
                    switch_key = 'off'
                    if self.verbose:
                        print "seq_list, init:", seq_list
                    running_list.append(self.sequential_evaluation(seq_list))
                    seq_list = []
                running_list.append(element)
            elif element == 'end':
                if switch_key == 'on':
                    switch_key = 'off'
                    if self.verbose:
                        print "seq_list, init:", seq_list
                    running_list.append(self.sequential_evaluation(seq_list))
                    seq_list = []
            else:
                if switch_key == 'on':
                    seq_list.append(element)
                if switch_key == 'off':
                    running_list.append(element)
        return self.sequential_evaluation(running_list)
    
    def evaluation(self, verbose=False):
        self.parser()
        running_list = []
        np_list_reversed = []
        for element in self.expression:
            if self.elementType(element) == 'rightParenthesis':
                while(True):
                    temp_element = running_list.pop()
                    if self.elementType(temp_element) != 'leftParenthesis':
                        np_list_reversed.append(temp_element)
                    else:
                        np_list = list(reversed(np_list_reversed))
                        if self.verbose:
                            print "np_list", np_list
                        running_list.append(self.no_parenthesis_evaluation(np_list))
                        np_list_reversed = []
                        np_list = []
                        break
            else:
                running_list.append(element)
        return self.no_parenthesis_evaluation(running_list)

#%%
e_obj = '( ( 1 + 2 ) + 3 )'
a_obj = arithmetic(e_obj)
a_obj.parser()
print a_obj.expression
print a_obj.evaluation()
print a_obj.operatorStack
print a_obj.valueStack            

#%%
e_obj = '( ( 1 + 2) + 3)'
a_obj = arithmetic(e_obj)
a_obj.parser()
print a_obj.expression
print a_obj.evaluation()
print a_obj.operatorStack
print a_obj.valueStack            

#%%
e_obj = '( ( 1 + 2.07235) + (3 + 0.00000)) + 3.0 + 4.0 '
a_obj = arithmetic(e_obj)
a_obj.parser()
print a_obj.expression
print a_obj.evaluation()
print a_obj.operatorStack
print a_obj.valueStack            

#%%
e_obj = ' 1 + (2.07235 + 3 + 0.00000 + 3.0 + 4.0 + 1.0*2.0/5.0 + 1.0*1.0*1.0 + 2.0*3*4)*4.0 + 2.99 - 1000'
a_obj = arithmetic(e_obj)
print a_obj.evaluation()
print eval(e_obj)
