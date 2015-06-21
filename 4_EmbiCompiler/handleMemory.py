# John Loeber | June 2015 | Python 2.7.9 | contact@johnloeber.com

# to handle the memory (i.e. data in a .mb file)

def getmem(mb):
    with open(mb,"r") as f:
        lines = f.readlines()
    memory = {}
    for x in lines:
        index = x.index("=")
        var = x[:index].lstrip(" ").rstrip(" ")
        spaceCheck(var)
        val = x[index+1:].rstrip(" ").lstrip(" ")
        memory[var] = val
    return memory
