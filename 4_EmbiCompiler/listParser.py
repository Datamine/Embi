# John Loeber | June 2015 | contact@johnloeber.com | Python 2.7.9

# Lists that contain ints and floats. 
# Lists are going to be static on this version of the program (with exception of mapping).
# If you need to do a list operation, like append or delete, just edit the data, where it is stored.

# Parses strings representing such lists into numeric python lists.

from numberParser import *

def evalList(x,memory):
    tokens = x[1:-1].split(",")
    parsed = [numParse(x,memory) for x in tokens]
    return parsed

def diff(small,big):
    # to prevent errors in > or < due to floating-point error
    #hopefully this epsilon will be small enough 
    if small < big - 0.00000001:
        return True
    else:
        False

def listParse(x,memory):
    def complain():
        print "Error! Purported list-expression cannot be parsed. Exiting."
        print "Offending Expression:", x
        exit(0)       
    # where x is a string
    x = x.replace(" ", "")
    temp = ""
    # first identify what we're dealing with: [a,b,c], map(f,[a,b,c]), range(a,b,c), or a variable name of a list in memory
    if x[0]=="[" and x[-1]=="]":
        return evalList(x,memory)

    elif x[0:3]=="map":
        sub = x[3:]
        if sub[0]=="(" and sub[-1]==")":
            sub = sub[1:-1]
            mapping = sub[:sub.index(",")]
            inputList = sub[sub.index(",")+1:]
            parsedList = listParse(inputList,memory)
            mapvariable = mapping[:mapping.index(":")]
            mapequation = mapping[mapping.index(":")+1:]
            mappedList = [numParse(mapequation.replace(mapvariable,str(item)),memory) for item in parsedList]
        else:
            complain()
        return mappedList
    elif x[0:5]=="range":
        sub = x[5:]
        if sub[0]=="(" and sub[-1]==")":
            parameters = evalList(sub,memory)
            if len(parameters)!=3:
                complain()
            generated = []
            current = parameters[0]
            end = parameters[1]
            step = parameters[2]
            if step > 0:
                while diff(current,end):
                    generated.append(current)
                    current = current+step
            else:
                while diff(end,current):
                    generated.append(current)
                    current = current+step
            return generated
        else:
            complain()
    elif x[0:4]=="list" and x[4:].isdigit() and x in memory.keys():
        return listParse(memory[x],memory)
    else:
        complain()
