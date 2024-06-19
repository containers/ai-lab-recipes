#!/usr/bin/env python3

import os
import sys

def isHuggingDir(elements):
	for n in s:
		if n.startswith(".hug"):
			return True
	return False

def printNonEmpty(*args):
	if len(args[0]) > 0:
		print(*args)

dir = sys.argv[1]
cwd = os.getcwd()
os.chdir(dir)
c = 0
result=""
for root, dirs, files in os.walk("."):
	s = root.split(os.path.sep)
	s.pop(0)
	if isHuggingDir(s):
		continue
	for file in files:
		if not file.endswith(".safetensors"):
			continue
		path = os.path.join("/run", ".input", "models", *s, file)
		partial = os.path.join("/usr", "share", "models", *s, file)
		cmd = f"rsync -ah --progress {path} {partial}"
		if c % 4 != 0:
			result = f"{result} \\\n\t && {cmd}"
		else:
			printNonEmpty(result)
			result = f"RUN {cmd}"
		c += 1
printNonEmpty(result)
os.chdir(cwd)
