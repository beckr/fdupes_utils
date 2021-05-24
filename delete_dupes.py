#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Delete all duplicates occurences (except one) from a CSV
CSV format needs to be /filepath/;hash <LF>
"""

__author__ = "rbeck"

import csv
from pprint import pformat

import os
import shutil
import logging
import hashlib

from optparse import OptionParser

deleted = 0
passed = 0

def load_csv(filepath):
	logging.debug("Entering load_csv with %s ", filepath)
	data = {}
	
	with open(filepath, "rb") as f:
		spamreader = csv.reader(f, delimiter=';', quotechar='"')
		for row in spamreader:
			if row:
				(filefullpath, hashfile) = row
				if hashfile:
					logging.debug("%s // %s" % (filefullpath, hashfile))

					if not data.has_key(hashfile):
						data[hashfile] = set()

					data[hashfile].add(filefullpath)

	logging.debug("="*20)
	logging.debug("Data are %s ", pformat(data))
	return data

def delete_files(data, simulate=False, check_hash=False):
	global deleted
	global passed
	logging.debug("="*20)
	logging.debug("Entering delete_files with %s data", len(data))

	if simulate is None:
		simulate = False

	if check_hash is None:
		check_hash = False	

	logging.debug("Simulate is set to %s", simulate)
	logging.debug("Check hash is set to %s", check_hash)


	for h, files in data.iteritems():

		valid_files = set()

		for f in files:
			if not os.path.exists(f):
				logging.info("The file %s does not exists", f)
			
			elif check_hash and hash_file(f) != h:
				logging.info("The hash for file %s does not match", f)	

			else:
				valid_files.add(f)

		if(len(valid_files) <= 1):
			logging.info("Zero or one valid item, do nothing (%s, %s)", h, valid_files)
			passed += 1

		for f in list(valid_files)[1:]:
			if simulate:
				logging.info("SIMULATE ON : %s candidate for deletion", f)
			else:
				try:
					os.remove(f)
					logging.info("File %s deleted", f)
					deleted += 1
				except OSError as e:
					logging.error("Error deleting file %s. Error was %s", f, e)



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


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-i", "--input", dest="input_file",
					  help="Input CSV file")

	parser.add_option("-s", "--simulate", action="store_true", dest="simulate",
					  help="Does nothing, just simulate actions")

	parser.add_option("-c", "--check-hash", action="store_true", dest="check_hash",
					  help="Should check the hash of the input file with the hash of the real file. The execution will be longer")

	parser.add_option("-l", "--log", dest="loglevel",
					  help="Set the log level. Add --log=INFO or --log=DEBUG for logging. The logging file will be in the same directory as delete_dupes.py and called delete_dupes.log")
					  
	(options, args) = parser.parse_args()

	if not options.input_file or not(os.path.exists(options.input_file)):
		print "-i option is mandatory, the path has to be valid"
		exit(-1)

	if options.loglevel is not None: 
		numeric_level = getattr(logging, options.loglevel.upper(), None)
		if not isinstance(numeric_level, int):
		    raise ValueError('Invalid log level: %s' % loglevel)
		logging.basicConfig(level=numeric_level, filename="delete_dupes.log", format='%(asctime)s:%(levelname)s:%(message)s')

	logging.info("="*80)
	logging.info("="*80)
	data = load_csv(options.input_file)
	delete_files(data, options.simulate, options.check_hash)
	logging.info("Done (Deleted: %s, Passed: %s)", deleted, passed)

