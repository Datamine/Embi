# John Loeber | June 2015 | contact@johnloeber.com | Python 2.7.9

# This is to parse simple arithmetic for ints and floats
# Supported operations: +, -, *, /, %, ^, sin, cos, int, float (typecasting) and () for order of operations
# Note that sin and cos are input in degrees. Division automatically casts to float.
# only alphabetic characters are legal for variable names, no spaces. Sin and Cos obviously illegal as variable names.

# TODO: clean up the style of this file

# TODO: add more/better error messages

from math import sin, cos,radians
from sys import exit

# Primitive Checks

# technique from http://stackoverflow.com/q/354038
def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def eval(x,tokens,memory):
    # evaluates a series of tokens given a particular memory.
    if tokens.count("(")!=tokens.count(")"):
        print "Error! A pair of parentheses is not closed. Exiting."
        print "Expression:", x
        exit(0)

    # replace variables with their equivalents from memory
    replaced = []
    for token in tokens:
        if isinstance(token,str):
            if token.isalpha() and token!="sin" and token!="cos" and token!="int" and token!="float":
                if token in memory.keys():
                    # have to cast to string in case memory token is non string (memory conventions are not yet set in stone)
                    value = numParse(str(memory[token]),memory)
                    replaced.append(value)
                else:
                    print "Error! Variable not in memory. Exiting."
                    print "Expression:", x
                    print "Variable:", token
                    exit(0)
            else:
                replaced.append(token)
        else:
            replaced.append(token)

    # reduce all parentheticals
    while "(" in replaced:
        firstClose = replaced.index(")")
        for i in range(firstClose,-1,-1):
            if replaced[i]=="(":
                openParen = i
                break
        subsequence = replaced[openParen+1 : firstClose]
        res = eval(x,subsequence,memory)
        replaced = replaced[0:openParen] + [res] + replaced[firstClose+1:]
        print replaced

    # now go through tokens and change any remaining string-form numbers to actual numbers
    for i in range(len(replaced)):
        el = replaced[i]
        if isinstance(el,str):    
            if isFloat(el):
                if isInt(el):
                    replaced[i] = int(el)
                else:
                    replaced[i] = float(el)

    # now parse raw tokens: int/float > sin/cos > exponentiation > multiplication = division = modulo > addition = subtraction
    # left associative where precedence is equal
    
    while "int" in replaced:
        ind = replaced.index("int")
        num = int(replaced[ind+1])
        replaced = replaced[0:ind] + [num] + replaced[ind+2:]

    while "float" in replaced:
        ind = replaced.index("float")
        num = float(replaced[ind+1])
        replaced = replaced[0:ind] + [num] + replaced[ind+2:]
    
    while "sin" in replaced:
        print replaced
        ind = replaced.index("sin")
        num = sin(radians(replaced[ind+1]))
        replaced = replaced[0:ind] + [num] + replaced[ind+2:]

    while "cos" in replaced:
        ind = replaced.index("cos")
        num = cos(radians(replaced[ind+1]))
        replaced = replaced[0:ind] + [num] + replaced[ind+2:]
    
    while "^" in replaced:
        i = replaced.index("^")
        num = replaced[i-1] ** replaced[i+1]
        replaced = replaced[0:i-1] + [num] + replaced[i+2:]
    
    while ("*" in replaced) or ("/" in replaced) or ("%" in replaced):
        for i in range(0,len(replaced)):
            if replaced[i]=="*":
                num = replaced[i-1] * replaced[i+1]
                replaced = replaced[0:i-1] + [num] + replaced[i+2:]
                break
            elif replaced[i]=="/":
                num = replaced[i-1] / float(replaced[i+1])
                replaced = replaced[0:i-1] + [num] + replaced[i+2:]
                break
            elif replaced[i]=="%":
                num = replaced[i-1] % replaced[i+1]
                replaced = replaced[0:i-1] + [num] + replaced[i+2:]
                break
     
    while ("+" in replaced) or ("-" in replaced):
        for i in range(0,len(replaced)):
            if replaced[i]=="+":
                num = replaced[i-1] + replaced[i+1]
                replaced = replaced[0:i-1] + [num] + replaced[i+2:]
                break
            elif replaced[i]=="-":
                num = replaced[i-1] - replaced[i+1]
                replaced = replaced[0:i-1] + [num] + replaced[i+2:]
                break   
    return replaced[0]

def numParse(x,memory):
    # where x is a string, and memory is a dict of variables
    x = x.replace(" ", "")
    tokens = []
    temp = ""
    # tokenize the string
    for c in x:
        if c.isdigit() or c==".":
            temp = temp + c
        elif c=="+" or c=="-" or c=="*" or c=="/" or c=="%" or c=="^" or c==")":
            tokens.append(temp)
            tokens.append(c)
            temp = ""
        elif c=="(":
            tokens.append(temp)
            tokens.append(c)
            temp = ""
        elif c.isalpha():
            temp = temp+c
        else:
            print "Error! Expression encountered that cannot be parsed. Exiting."
            print "Offending Expression:", x
            print "Offending Portion:", temp
            print "Character:", c
            exit(0)

    tokens.append(temp)
    tokens = filter(lambda x: x!="", tokens)
    return eval(x,tokens,memory)
