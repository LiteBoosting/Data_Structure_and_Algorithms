#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy

#%%
class arithmetic(object):
    """Return evaluation of a given arithmetic expression (stored as a string).
    As version-2, this solver has less contraints than version-1:
    1. Only numbers (int or float), 4 basic operators (+, -, *, /), and left/right
       parentheses are effective elements. (still true)
    2. There should be a seperator (single space) between each effective element in the string. (false,
       intelligent parsing has been implemented)
    3. There is no consideration of operation priority among '+', '-' and '*', '/', i.e.,
       every operation of two numbers should be embraced by a pair of parentheses. (false, priority has
       been considered in a proper way)
    4. This is an implementation of the so-called two-stack algorithm:
        1. Value: push onto the value stack.
        2. Operator: push onto the operator stack.
        3. Left parenthesis: ignore.
        4. Right parenthesis: pop operator and two values;
        5. Push the result of applying that operator to those values onto the operand stack.
        (false, new algorithm has been implemented)
    5. The algorithm for version-2 contains the following steps:
        1. Values, operators and parentheses are in the same stack.
        2. Whenever we meet right parenthesis, pop out elements until we pop one and exactly one left
           parenthesis.
        3. Apply the no_parth_eval() function on poped sublist.
        4. When we touch the end of the list, implement the no_parth_eval() on the whole list.
        5. no_parth_eval(): go through operators in the sublist, if see either * or /, then
           go through until we see a + or -, or touch the end of sub_list, then pop this segment out and
           apply the seq_eval(), return the value to the sub_stack and go on to find next
           prioritied segment (continuous * or /). When we touched the end of sub_list, implement the
           seq_eval() on the whole sub_list.
    """
    
    def __init__(self, expression, verbose=False):
        self.raw_expression = expression
        self.valueStack = []
        self.operatorStack = []
        self.verbose = verbose
        if self.verbose:
            self.indent = 0
        
    def parsing(self):
        """ Parse the string to a list, with each element ((, +, -, *, /, number)) as one entry in the list.
        """
        if self.verbose:
            print(' '*self.indent + "Before parsing: " + self.raw_expression)
        self.expression = []
        number_record = ''
        i = 0
        size = len(self.raw_expression)
        for char in self.raw_expression:
            i += 1
            if char in ('(', ')', '+', '-', '*', '/'):
                # if we see one of these characters, we know that the number series ends, therefore we
                # record the number series as one element. We also record character here as one element
                if number_record != '':
                    self.expression.append(number_record)
                    number_record = ''
                self.expression.append(char)
            elif char in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'):
                # if we see one of these characters, we know that we are going through a number, so we
                # won't stop to record, we append it to number_record
                number_record += char
            else:
                # if we see other type of characters, we ignore it, and we know the number series ends
                if number_record != '':
                    self.expression.append(number_record)
                    number_record = ''
            if (i == size) and (number_record != ''):
                self.expression.append(number_record)
                number_record = ''
        if self.verbose:
            print(' '*self.indent + "After parsing: ", self.expression)
            
    def element_type(self, element):
        """Return the type of element.
        number, operator, leftParenthesis, rightParenthesis.
        """
        if element == '(':
            return 'leftParenthesis'
        elif element == ')':
            return 'rightParenthesis'
        elif element in ('+', '-', '*', '/'):
            return 'operator'
        elif element[0] in ('.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            return 'number'
        else:
            return 'unknown'
            
    def bi_eval(self, number1, number2, operator):
        """Return value of the operation on the two values.
        """
        if operator == '+':
            return str(float(number1) + float(number2))
        elif operator == '-':
            return str(float(number1) - float(number2))
        elif operator == '*':
            return str(float(number1) * float(number2))
        elif operator == '/':
            return str(float(number1) / float(number2))
        
    def seq_eval(self, seq_list):
        """Evaluate an expression with sequential priorities, i.e., no parenthesis to change priority and
        no mixed priority between (*, /) and (+, -)
        """
        if self.verbose:
            self.indent += 4
            print(' '*self.indent + 'Begin sequential evaluation for: '+ ' '.join(seq_list))
        seq_list = deepcopy(seq_list)
        if len(seq_list) == 1:
            if self.element_type(seq_list[0]) == 'number':
                return seq_list[0]
            else:
                raise ValueError('value error:' + '(' + seq_list[0] + ')')
        while len(seq_list) > 1:
            value1 = seq_list.pop(0)
            operator = seq_list.pop(0)
            value2 = seq_list.pop(0)
            seq_list.insert(0, self.bi_eval(value1, value2, operator))
            if self.verbose:
                print(' '*self.indent + "seq_list:", seq_list)
        if self.verbose:
            print(' '*self.indent + 'End sequetial evaluation')
            self.indent -= 4
        return seq_list[0]
    
    def no_parth_eval(self, no_parth_list):
        """Evaluate an expression without any parenthesis.
        """
        if self.verbose:
            self.indent += 4
            print(' '*self.indent + 'Begin no parenthesis evaluation for: ' + ' '.join(no_parth_list))
        if len(no_parth_list) == 1:
            if self.element_type(no_parth_list[0]) == 'number':
                return no_parth_list[0]
            else:
                raise ValueError('value error:' + '(' + no_parth_list[0] + ')')
        running_list = [] # use this list as a stack for evaluation
        seq_list = [] # extract sequential list and do evaluation
        is_recording = False # False means we do not record current element to seq_list, True means we do
        for element in no_parth_list:
            if element in ('*', '/'):
                if not is_recording:
                    # means that this is the first time we see * or /, we would begin recording,
                    # also extract the number efore this operator
                    is_recording = True
                    seq_list.append(running_list.pop())
                seq_list.append(element)
            elif element in ('+', '-'):
                if is_recording:
                    # means that this is the first time we see + or -, we would stop the recording,
                    # evaluate the seq_list, and append its result to running_list
                    is_recording = False
                    running_list.append(self.seq_eval(seq_list))
                    seq_list = []
                running_list.append(element)
            elif self.element_type(element) == 'number':
                if is_recording:
                    seq_list.append(element)
                if not is_recording:
                    running_list.append(element)
            else:
                raise ValueError('value error:' + '(' + element + ')')
            if self.verbose:
                print(' '*self.indent+'Running list: '+' '.join(running_list)+", sequential list: "+' '.join(seq_list))
        # at the end of no_parth_list
        if is_recording:
            is_recording = False
            running_list.append(self.seq_eval(seq_list))
            seq_list = []
            if self.verbose:
                print(' '*self.indent+'Running list: '+' '.join(running_list)+", sequential list: "+' '.join(seq_list))
        # evaluate the whole running_list and return the value
        return_value = self.seq_eval(running_list)
        if self.verbose:
            print(' '*self.indent + 'End no parenthesis evaluation')
            self.indent -= 4
        return return_value
    
    def main_eval(self):
        self.parsing()
        running_list = []
        no_parth_list = []
        if self.verbose:
            print('Begin main evaluation for: ' + ' '.join(self.expression))
        for element in self.expression:
            if self.element_type(element) == 'rightParenthesis':
                while(True):
                    popped_element = running_list.pop()
                    if self.element_type(popped_element) != 'leftParenthesis':
                        no_parth_list.insert(0, popped_element)
                    else:
                        if self.verbose:
                            print("Runing list: "+' '.join(running_list)+", no_parth_list: "+' '.join(no_parth_list))
                        running_list.append(self.no_parth_eval(no_parth_list))
                        no_parth_list = []
                        break
            else:
                running_list.append(element)
            if self.verbose:
                print("Runing list: "+' '.join(running_list)+", no_parth_list: "+' '.join(no_parth_list))
        return float(self.no_parth_eval(running_list))

#%%
e_obj = '( ( 1 + 2 ) + 3 )asdf'
a_obj = arithmetic(e_obj, verbose=True)
print(a_obj.main_eval())

#%%
e_obj = '( ( 1 + 2.07) + (3 + 0.0)) + 3.0 + 4.0 '
a_obj = arithmetic(e_obj, verbose=True)
print(a_obj.main_eval())

#%%
e_obj = ' 1 + (2.07 + 3 + 0.0 + 3.0 + 4.0 + 1.0*2.0/5.0 + 1.0*1.0*1.0 + 2.0*3*4)*4.0 + 2.99 - 1000'
a_obj = arithmetic(e_obj, verbose=True)
print(a_obj.main_eval())

#%%
e_obj = ' 1 + (2.07 + 3 + 0.0 + 3.0 + 4.0 + 1.0*2.0/5.0 + 1.0*1.0*1.0 + 2.0*3*4)*4.0 + 2.99 - 1000'
a_obj = arithmetic(e_obj, verbose=False)
print(a_obj.main_eval())
print("evaluation from python built-in eval() function:", eval(e_obj))
