"""-----------------------------------------------------------------------------

	io.py - LR, November 2016

	Provides some I/O routines, tailored for numerical evaluation.

	STATUS:
	Currently not failsafe when a non-numerical line is detected. This needs to
	be implemented.

-----------------------------------------------------------------------------"""
import os, sys, re, time, datetime

class color:
	"""	Format specifiers for sophisticated output.
	"""
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'

	def wrap(value, label):
		return label + str(value) + END


"""-----------------------------------------------------------------------------
						 DIRECTORY OPERATIONS
-----------------------------------------------------------------------------"""
def dirWalk(pattern):
	"""	Creates a list of subdirectories which all contain a specified pattern.
	"""
	return sorted([root + "/" for root, dirs, _ in os.walk(os.getcwd()) if re.search(pattern, root) and len(dirs) == 0])


def fastWalk(root, pattern):
	"""	Creates a list of subdirectories which all contain a specified pattern.
		[Meant to be a faster version of dirWalk() but performs only marginally
		better.]
	"""
	subDirs = [f for f in os.listdir(root) if os.path.isdir(root + "/" + f) and f[0] != '.']
	if subDirs:
		return filter(None, [fastWalk(root + "/" + sd, pattern) for sd in subDirs])
	else:
		if re.search(pattern, root):
			return root + "/"


def removeTopDirectory(path, n=2):
	"""	Removes the last directory in a path.
	"""
	subs = path.split('/')
	newPath = ''
	for k in range(0, len(subs) - n):
		newPath += subs[k] + '/'
	return newPath


def createNestedDir(path):
	""" Creates a directory and all directories along the path.
	"""
	subs = filter(None, path.split('/'))
	subPath = ""
	if path[0] == "/":
		subPath = "/"
	for sub in subs:
		subPath += sub + "/"
		if not os.path.isdir(subPath):
			os.makedirs(subPath)


def getDirSize(folder):
	""" Returns the size of the folder recursively.
	"""
	tot_size = os.path.getsize(folder)
	for item in os.listdir(folder):
		itempath = os.path.join(folder, item)
		if os.path.isfile(itempath):
			tot_size += os.path.getsize(itempath)
		elif os.path.isdir(itempath):
			tot_size += getDirSize(itempath)
	return tot_size


def getDirFiles(folder, start = ""):
	"""	Retrieves a list of files in a directory. A pattern which needs to be
		matched can be specified.
	"""
	l = []
	for root, dirs, files in os.walk(folder):
		for fil in files:
			if fil.startswith(start):
				l.append(root + "/" + fil)
	return l


def makeDir(path):
	"""	Creates a folder if it is not existent and asks for further steps if it
		is.
	"""
	if not os.path.exists(path):
		os.makedirs(path)
	else:
		print("Output folder already exists - Continue? [y/n]")
		opt = ''
		while True:
			opt = raw_input()
			if opt == 'n':
				print('TERMINATING')
				sys.exit()
			elif opt == 'y':
				break
			else:
				print('Please enter valid option. [y/n]')


"""-----------------------------------------------------------------------------
							FILE OPERATIONS
-----------------------------------------------------------------------------"""
def getFileLines(path, head = 0, cutoff = 0):
	"""	Reads all the lines in a file and returns then as a list. Cuts the first
		head lines.
	"""
	with open(path) as h:
		raw = h.readlines()
		if cutoff:
			raw = raw[head:cutoff]
		else:
			raw = raw[head:]
		return raw


def getFileNumberLines(path, head = 0, cutoff = 0):
	"""	Reads all the lines in a file and returns lines in the form of splitted
		and converted numerical values. Cuts the first head lines.
		Stops after cutoff lines.
	"""
	with open(path) as h:
		raw = h.readlines()[head:]
	if not cutoff:
		cutoff = len(raw)
	return [splitNumbersLine(rawLine) for rawLine in raw[:cutoff]]


def getFileNumbersInDict(path, keys, head = 0):
	"""	Reads all the lines in a file and returns a dictionary with the
		specified amount of keys, which will be the first entries in each line.
		Cuts the first head lines.
	"""
	lineDict = dict()
	with open(path) as h:
		for rawLine in h.readlines()[head:]:
			line = splitNumbersLine(rawLine)
			lineDict[tuple(line[0:keys])] = line[keys:]
	return lineDict


def appendLine(path, line):
	""" Appends a line to a given file.
	"""
	with open(path, 'a') as h:
		h.write(line + "\n")


def writeNumbersFile(path, data, header = None):
	""" Takes a filename and a list of numerical data and creates a file with
		the linewise data.
	"""
	with open(path, 'w') as h:
		if header is not None:
			h.write(header + "\n")
		for line in data:
			for k in range(len(line)):
				h.write("{:.10f}\t\t".format(line[k]))
			h.write('\n')


def writeFile(path, text):
	""" Takes a filename and a list of lines and writes it to a file.
	"""
	with open(path, 'w') as h:
		for line in text:
			h.write(line + '\n')



"""-----------------------------------------------------------------------------
								MISC
-----------------------------------------------------------------------------"""
def splitLine(line):
	"""	Splits a string at all whitespaces and removes empty entries.
	"""
	return filter(None, re.split("\s", line))

def splitNumbersLine(line):
	"""	Splits a string into floats and removes empty entries.
		ATTENTION:	Might throw a ValueError.
	"""
	res = []
	for rawVal in splitLine(line):
		try:
			res.append(float(rawVal))
		except ValueError:
			res.append(rawVal)
	return res

def timestamp(f = None):
	"""	Returns current time in the specified format.
	"""
	if f is None:
		return datetime.datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
	else:
		return datetime.datetime.now().strftime(f)