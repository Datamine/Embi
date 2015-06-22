# John Loeber | June 2015 | Python 2.7.9 | contact@johnloeber.com

# to handle the memory (i.e. data in a .mb file)

from sys import exit

def spaceCheck(var):
    if " " in var:
        print "Error! There is a space in variable:" + var + " Spaces not allowed in variable names. Exiting."
        exit(0)
    elif not var.isalnum():
        print "Error! Variable name: " + var + " is not alphanumeric. Exiting."
        exit(0)
    else:
        return

def getmem(mb):
    with open(mb,"r") as f:
        lines = f.readlines()
    memory = {}
    for x in lines:
        index = x.index("=")
        var = x[:index].rstrip("\r\n").lstrip(" ").rstrip(" ")
        spaceCheck(var)
        val = x[index+1:].rstrip("\r\n").rstrip(" ").lstrip(" ")
        memory[var] = val
    return memory
