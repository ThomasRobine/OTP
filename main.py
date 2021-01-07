# -*- coding:utf-8 -*-

import os
from os import walk
import argparse
import subprocess


def check_interface():
	''' (NoneType) -> NoneType

	>>> check_interface()
	Network interface is up, now exiting ...
	'''
	for root, directories, files in walk("/sys/class/net/"):
		for directory in directories:
			file = open("/sys/class/net/"+directory+"/operstate", 'r')
			for state in file:
				if state == 'up\n':
					exit('Network interface is up, now exiting ...')
	

def create_file(file_path, bytes):
	''' (String, bytes) -> NoneType

	create_files('Directories/0000/00p', 48)
	>>>
	'''
	writer = open(file_path, 'w')
	random_list = []
	'''
	takes too much time
	file = open('/dev/random','rb')
	for x in file.read(bytes):
		random_list.append(bin(ord(chr(x)))[2:].zfill(8))
	file.close()
	'''
	for i in range(bytes):
		random = os.urandom(1)
		random_list.append(bin(ord(random))[2:].zfill(8))
	writer.write(''.join(random_list))

def generate_pads(directory_path):
	''' (String) -> NoneType

	generate_pads('Directories/OOOO/')
	>>>
	'''
	count = 0
	while count < 100:
		if len(str(count)) < 2:
			filename_prefix = str(0)+str(count)+'p'
			create_file(directory_path+filename_prefix, 48)

			filename_pad = str(0)+str(count)+'c'
			create_file(directory_path+filename_pad, 2000)

			filename_suffix = str(0)+str(count)+'s'
			create_file(directory_path+filename_suffix, 48)
		else:
			filename_prefix = str(count)+'p'
			create_file(directory_path+filename_prefix, 48)

			filename_pad = str(count)+'c'
			create_file(directory_path+filename_pad, 2000)

			filename_suffix = str(count)+'s'
			create_file(directory_path+filename_suffix, 48)
		count += 1

def generate(directory_path):
	''' (String) -> NoneType

	generate('Directories/')
	>>>
	'''
	for root, directories, files in walk(directory_path):
		if len(directories) == 0:
			subprocess.call(['mkdir', '--', directory_path+'0000'], shell = False)
			generate_pads(directory_path+'0000/')
		else:
			count = 0
			missing = False
			dirs = directories
			dirs = dirs.sort()
			for directory in directories:
				directory_num = int(directory)
				if directory_num != count:
					if len(str(count)) == 1:
						directory_path += '000'+str(count)
					elif len(str(count)) == 2:
						directory_path += '00'+str(count)
					elif len(str(count)) == 3:
						directory_path += '0'+str(count)
					else:
						directory_path += str(count)
					subprocess.call(['mkdir', '--', directory_path], shell = False)
					generate_pads(directory_path+'/')
					missing = True
					break
				count += 1
			if not missing and count != 9999:
				if len(str(count)) == 1:
					directory_path += '000'+str(count)
				elif len(str(count)) == 2:
					directory_path += '00'+str(count)
				elif len(str(count)) == 3:
					directory_path += '0'+str(count)
				else:
					directory_path += str(count)
				subprocess.call(['mkdir', '--', directory_path], shell = False)
				generate_pads(directory_path+'/')
		break

def sanity_check(message):
	''' (String) -> Boolean

	sanity_check('Hello')
	>>> True
	'''
	if len(message) <= 2000:
		return True
	return False

def get_pad(directory_path):
	''' (String) -> String

	get_pad()
	>>> '0000/00c'
	'''
	for root, directories, folders in walk(directory_path):
		dirs = directories
		dirs = dirs.sort()
		for directory in directories:
			for path, repo, files in walk(directory_path+directory):
				f = files
				f = f.sort()
				for file in files:
					if 'c' in file:
						return directory_path+directory+'/'+file
		exit('No pads available, generate a new folder ...')
		
def encrypt_text(text):
	''' (String) -> list of binaries

	>>> ecnrypt_message('Hello!')
	0110100001100101011011000110110001101111001000010010001100100011001000110010001100100011
	'''
	return ''.join([format(ord(i), "08b") for i in text])

def send(args):
	''' (String, String) -> NoneType

	send(Nonetype, NoneType)
	>>>
	'''
	text = ""
	if args.file != None:
		file = open(args.file, 'r')
		text = file.read()
	elif args.text != None:
		text = args.text
	else:
		text = input('Enter text to encrypt : ')
	if sanity_check(text):
		pad = get_pad(args.directory)
		original_pad = pad
		encrypted_text = encrypt_text(text)
		prefix_file = open(pad[:-1]+'p', 'r')
		prefix = prefix_file.read()
		suffix_file = open(pad[:-1]+'s', 'r')
		suffix = suffix_file.read()
		pad = pad[:-1]+'t'
		pad = pad.split('/')
		writer = open(pad[0]+'-'+pad[1]+'-'+pad[2], 'w')
		writer.write(str(prefix)+str(encrypted_text)+str(suffix))
		subprocess.call(['shred', '-u', original_pad], shell = False)
	else:
		exit('The message can not fit in the pad')

def receive():
	py = 0

def todo():
	''' (NoneType) -> NoneType

	todo()
	>>>
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', dest = 'directory', required = True)
	parser.add_argument('-g', dest = 'generate', action = 'store_true')
	parser.add_argument('-s', dest = 'send', action = 'store_true')
	parser.add_argument('-f', dest = 'file')
	parser.add_argument('-t', dest = 'text')
	parser.add_argument('-r', dest = 'receive', action = 'store_true')
	args = parser.parse_args()
	if args.send != False:
		send(args)
	elif args.receive != False:
		receive()
	else:
		generate(args.directory)

if __name__ == "__main__":
	#check_interface()
	todo()