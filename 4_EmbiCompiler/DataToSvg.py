# John Loeber | May 2015 | Python 2.7.x | Embi Project: www.github.com/datamine/Embi | contact@johnloeber.com

# this is a small script that given an Embi data file (via the command line), converts the data to a .svg document. 
# To see examples of Embi data files, look in the folder "2_Examples". Specifically, a data file is one
# line of canvas information followed by any number of lines of element information. In this toy implementation
# of Embi, we only have three elementary types of visual element, described as such:
#	* rect(w,h,x,y,color,opacity,rotation,xstretch,ystretch)
#	* circle(r,x,y,color,opacity,rotation,xstretch,ystretch)
#		(note: stretches are applied before rotation.)
#	* space(w,h,x,y)
#	where 	w,h,x,y are given in px, rotation in degrees, xstretch and ystretch are floats,
#		color is a hex code, and opacity is a value between 0.0 and 1.0.

# note: overlap order is determined numerically, i.e. the smallest-ranked elements (element1, element2, etc.) are
# the furthest "back", and the highest-numbered elements are the furthest front.

# note: assumption is that an Embi data file ends in an extension .mb. 
# All of this will be eventually tranposed to a web application -- working with files is only for the purpose
# of having some sort of demoable version.

# Important note: the .svg output by this file is the type of svg that is really meant to be included
# in HTML, as shown on http://www.w3schools.com/svg/svg_inhtml.asp. Need to change to the svg format
# as shown on http://commons.wikimedia.org/wiki/SVG_examples. A little additional formatting is necessary.

# TODO: Need to change langspec for VEs: circles should be denoted circ(...) not circle(...).
# (also change appropriately here. Or use circl, and standardize to five letters. in any case,
# a standard length for the VE identifier would be good.

# TODO: parseCanvas/Element/Circ/Rect are all similar (esp. circ and rect). It'd be good to unify them
# in one or a few general function(s).

# TODO: this file needs to be re-styled (obey the 80char limit, etc.). Currently quite ugly.

# TODO: there's no need to parse spaceholders -- should just filter them out along with comments

# TODO: implement the "rotation" feature. (A little trickier since it requires an order of operations.)
# Maybe use SVG ellipse? (Also implement stretching!)

import sys

def parseCanvas(line):
	def throwCanvasError():
		sys.stderr.write("Error! Canvas initialization line is incorrectly formatted.\n")
		sys.exit(1)
	# remove whitespace
	line = line.replace(" ", "")
	# sanity check the input
	elementCounts = [line.count(x) for x in [",","=",":","(",")","w","h"]]
	if elementCounts != [1,1,2,1,1,1,1]:
		throwCanvasError()
	
	leftstrip = line[line.index("(")+1:]
	# take out return carriages as well, just in case.
	rightstrip = leftstrip.rstrip(")\r\n")
	# split into two parts, find out which assigns width and which assigns height:
	widthAndHeight = rightstrip.split(",")
	# sanity check these parts
	if [rightstrip.count(x) for x in ["w:","h:"]]!= [1,1] or ("w:" in widthAndHeight[0] and "w:" in widthAndHeight[1]) or ("h:" in widthAndHeight[0] and "h:" in widthAndHeight[1]) :
		throwCanvasError()
	for part in widthAndHeight:
		if "w:" in part:
			width = part.replace("w:","")
		if "h:" in part:
			height = part.replace("h:","")
	if (width.isdigit(),height.isdigit()) != (True,True):
		sys.stderr.write("Error! Processing the canvas initialization line resulted in a non-integer value.\n")
		sys.stderr.write("Resultant width: " + width + ", height: " + height + "\n")
		sys.exit(1)
	outline = '<svg width ="'+str(width)+'" height ="'+str(height) + '">\n'
	return outline

def isInt(string):
	# adapted from http://stackoverflow.com/q/354038	
	try:
		int(string)
		return True
	except ValueError:
		return False

def isFloat(string):
	# adapted from http://stackoverflow.com/q/354038	
	try:
		float(string)
		return True
	except ValueError:
		return False

def isGoodHex(string):
	# adapted from http://stackoverflow.com/a/11592279
	try:
		if 0 <= int(string,16) <= 16777215:
			return True
		else:
			return False
	except ValueError:
		return False

def parseRect(line):
	def throwRectError():
		sys.stderr.write("Error! Rectangle initialization line is incorrectly formatted.\n")
		sys.stderr.write("Line: " + line)
		sys.exit(1)
	# note whitespace has already been removed. sanity check:
	elementCounts = [line.count(x) for x in [",","=",":","(",")"]]
	if elementCounts!= [8,1,9,1,1]:
		throwRectError()
	# format
	line2 = line[line.index("=")+1:]
	leftstrip = line2[line2.index("(")+1:]
	rightstrip = leftstrip.rstrip(")\r\n")	
	split = rightstrip.split(",")
	# sanity check the parts of the split
	# .. had done this incorrectly. need to write a function that checks for a bijection between the parts
	# and the properties of the VE.
	#partCounts = [split.count(x) for x in ["w:","h:","x:","y:","color:","opacity:","rotation:","xstretch:","ystretch:"]]
	#if partCounts != [1, 1,1,1,1, 1,1,1,1]:
	#	throwRectError()
	for part in split:
		if "w:" in part:
			w = part.replace("w:","")
		elif "x:" in part:
			x = part.replace("x:","")
		elif "color:" in part:
			color = part.replace("color:","")
		elif "opacity:" in part:
			opacity = part.replace("opacity:","")
		elif "rotation:" in part:
			rotation = part.replace("rotation:","")
		elif "xstretch:" in part:
			xstretch = part.replace("xstretch:","")
		elif "ystretch:" in part:
			ystretch = part.replace("ystretch:","")
		elif "h:" in part:
			h = part.replace("h:","")
		elif "y:" in part:
			y = part.replace("y:","")

	check = (isInt(x),isInt(y),isInt(w),isInt(h),isFloat(rotation),isFloat(xstretch),isFloat(ystretch),isFloat(opacity),isGoodHex(color))
	if check!=(1,1,1,1,1, 1,1,1,1):
		throwRectError()
	out = '<rect x="' + x +'" y="' + y + '" width="' + w + '" height="' + h + '" style="fill:#' + color + ";fill-opacity:" + opacity + ';"/>\n'
	return out


def parseCircle(line):
	def throwCircleError():
		sys.stderr.write("Error! Circle initialization line is incorrectly formatted.\n")
		sys.stderr.write("Line: " + line)
		sys.exit(1)
	# note whitespace has already been removed. sanity check:
	elementCounts = [line.count(x) for x in [",","=",":","(",")"]]
	if elementCounts!= [7,1,8,1,1]:
		throwCircleError()
	# format
	line2 = line[line.index("=")+1:]
	leftstrip = line2[line2.index("(")+1:]
	rightstrip = leftstrip.rstrip(")\r\n")	
	split = rightstrip.split(",")
	# sanity check the parts of the split
	# .. similar error as in parseRect.
	#partCounts = [split.count(x) for x in ["r:","x:","y:","color:","opacity:","rotation:","xstretch:","ystretch:"]]
	#if partCounts != [1,1,1,1, 1,1,1,1]:
	#	throwCircleError()
	for part in split:
		if "color:" in part:
			color = part.replace("color:","")
		elif "r:" in part:
			r = part.replace("r:","")
		elif "x:" in part:		
			x = part.replace("x:","")
		elif "opacity:" in part:
			opacity = part.replace("opacity:","")
		elif "rotation:" in part:
			rotation = part.replace("rotation:","")
		elif "xstretch:" in part:
			xstretch = part.replace("xstretch:","")
		elif "ystretch:" in part:
			ystretch = part.replace("ystretch:","")
		elif "y:" in part:
			y = part.replace("y:","")

	check = (isInt(x),isInt(y),isFloat(r),isFloat(rotation),isFloat(xstretch),isFloat(ystretch),isFloat(opacity),isGoodHex(color))
	if check!=(1,1,1,1, 1,1,1,1):
		throwCircleError()
	out = '<circle cx="' + str(int(x)+int(r)) +'" cy="' + str(int(y)+int(r)) + '" r="' + str(r) + '" style="fill:#' + color + ";fill-opacity:" + opacity + ';"/>\n'
	return out

def parseElement(line):
	# remove whitespace
	line = line.replace(" ", "")
	line2 = line[line.index("=")+1:]
	if line2[:4]=="spac":
		# there's nothing to be done for a spaceholding element. Spaceholders only exist to affect group operations.
		return
	elif line2[:4]=="circ":
		return parseCircle(line)
	elif line2[:4]=="rect":
		return parseRect(line)
	else:
		sys.stderr.write("Error! Line is specifying an unknown type of visual element.\n")
		sys.stderr.write("Problematic line: " + line)
		sys.exit(1)

def toSvg(infile):
	# outfile is a correctly-ordered list of lines to be written to the svg file.
	outfile = []
	# grab the lines in in the input-file. We can expect this to be small, so we do it all at once.
	with open(infile,"r") as f:
		allLines = f.readlines()
	# filter out the comments (identified by starting with an octothorpe) and blank lines.
	allLines = [x for x in allLines if (x[0]!="#" and len(set(x))>3)]

	# check for the canvas initialization as the first line.	
	if "canvas" in allLines[0]:
		outfile.append(parseCanvas(allLines[0]))
		allLines = allLines[1:]
	else:
		sys.stderr.write("Error! Canvas description is not the first non-comment line.\n")
		sys.exit(1)

	# now sort the lines by element number so we get the right overlap order.
	allLines.sort()

	# now parse over the rest of the lines. Each line yields a new svg element.
	for line in allLines:
		convertedToSvg = parseElement(line)
		# check for None in case we're parsing a spaceholder.
		if convertedToSvg!=None:
			outfile.append(convertedToSvg)

	outfile.append("</svg>")
	return outfile

def main():
	# handling input/output. The actual conversion of input to output happens in toSvg().
	input = sys.argv[1]
	if input[-3:]!='.mb':
		sys.stderr.write("Error! File supplied is not an Embi data file.\n")
		sys.exit(1)

	output = input[:-3] + ".svg"
	svg = toSvg(input)
	with open(output,"w") as f:
		for line in svg:
			f.write(line)
		f.close()

if __name__=='__main__':
	main()
