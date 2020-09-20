from VMContents import *
from Parser import Parser
from CodeWriter import CodeWriter
import glob
import argparse
import os.path

def main():
    if len(sys.argv) != 2:
		print('Usage:Assembler file.vm')
	else:
		infile = sys.argv[1]
    
    if infile.endswith('.vm')