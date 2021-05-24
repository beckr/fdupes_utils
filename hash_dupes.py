#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Output CSV file with file & hash for each found file
"""

__author__ = "rbeck"

import csv
import os
import shutil
import logging
import hashlib

from optparse import OptionParser

BLOCK_SIZE = 65536 # The size of each read from the file

def hash_file(filepath):
	logging.debug("Entering hash_file with %s ", filepath)
	if os.path.exists(filepath):
		file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
		with open(filepath, 'rb') as f: # Open the file to read it's bytes
		    fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
		    while len(fb) > 0: # While there is still data being read from the file
		        file_hash.update(fb) # Update the hash
		        fb = f.read(BLOCK_SIZE) # Read the next block from the file

		hash_result = file_hash.hexdigest()
		logging.debug("Hash for %s is %s", filepath, hash_result)
		return hash_result # Get the hexadecimal digest of the hash
	else:
		logging.debug("File %s doesn't exist", filepath)

def load_files(filepath):
	logging.debug("Entering load_files with %s ", filepath)
	data = []
	with open(filepath, "r") as f:
		content = f.read()
		if content is not None:
			data = [d for d in content.split("\n") if d is not None]
	logging.debug("Data are %s ", data)
	return data

def create_output_file(filepath, data):
	logging.debug("Entering create_output_file with %s filepath and %d data", filepath, len(data))
	with open(filepath, "wb") as f:
		for d in data:
			logging.debug("Writing %s row", d)
			spamwriter = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow(d)
    	

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-i", "--input", dest="input_file",
					  help="Input file (list of full file paths separated by line feed)")

	parser.add_option("-o", "--output", dest="output_file",
					  help="Output CSV file full path")

	parser.add_option("-l", "--log", dest="loglevel",
					  help="Add --log=INFO or --log=DEBUG for logging")
					  
	(options, args) = parser.parse_args()

	if not options.input_file or not(os.path.exists(options.input_file)):
		print "-i option is mandatory, the path has to be valid"
		exit(-1)

	if not options.output_file:
		print "-o option is mandatory, the path has to be valid"
		exit(-1)

	if options.loglevel is not None: 
		numeric_level = getattr(logging, options.loglevel.upper(), None)
		if not isinstance(numeric_level, int):
		    raise ValueError('Invalid log level: %s' % loglevel)
		logging.basicConfig(level=numeric_level, format='%(asctime)s:%(levelname)s:%(message)s')

	files = load_files(options.input_file)
	data = [(fp, hash_file(fp)) for fp in files]
	create_output_file(options.output_file, data)
