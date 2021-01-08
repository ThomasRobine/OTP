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
					file.close()
					exit('Network interface is up, now exiting ...')
			file.close()
	

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
	writer.close()

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
	if not os.path.exists(directory_path):
		subprocess.call(['mkdir', '--', directory_path], shell = False)
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
		
def text_to_binary(text):
	''' (String) -> list of binaries

	>>> ecnrypt_message('Hello!')
	0110100001100101011011000110110001101111001000010010001100100011001000110010001100100011
	'''
	return ''.join([format(ord(i), "08b") for i in text])

def get_pad_needed(binary_text, binary_key):
	''' (String, String) -> String

	get_pad_needed('01101000', '0101101011010010')
	>>> '01011010'
	'''
	return binary_key[:-(len(binary_key)-len(binary_text))]

def get_bytes(binary_key):
	''' (String) -> list of String

	get_bytes('0101010101010101')
	>>> ['01010101', '01010101']
	'''
	return [binary_key[i: i+8] for i in range(0, len(binary_key), 8)]

def bytes_to_b10(bytes_key):
	''' (list of String) -> list of int

	bytes_to_b10(['01010101', '01010101'])
	>>> [7, 7]
	'''
	return [int(byte, 2) for byte in bytes_key]

def get_ascii(element):
	''' () -> list of ascii values

	get_ascii('hello'):
	>>> [15, 4, 25, 25, 34]
	'''
	return [ord(str(elem)) for elem in element]

def encrypt_text(text, pad):
	''' (list of int, list of int) -> list of int

	encrypt_text([15, 4, 25, 25, 34], [12, 23, 26, 54, 76])
	>>> [229, 229, 55, 167, 146]
	'''
	return [(text[i]+pad[i])%256 for i in range(len(text))]

def int_to_binary(encrypted_text):
	''' (list of int) -> list of binaries

	>>> intToBinary([242, 244, 241, 255])
	[11110010, 11110100, 11110001, 11111111]
	'''
	return [format(i, "08b") for i in encrypted_text]

def send(args):
	''' (String, String) -> NoneType

	send(Nonetype, NoneType)
	>>>
	'''
	text = ""
	if args.file != None:
		file = open(args.file, 'r')
		text = file.read()
		file.close()
	elif args.text != None:
		text = args.text
	else:
		text = input('Enter text to encrypt : ')
	if sanity_check(text):
		pad_path = get_pad(args.directory)
		pad_file = open(pad_path, 'r')
		pad_value = pad_file.read()
		pad_file.close()
		pad_needed = get_pad_needed(text_to_binary(text), pad_value)
		print('pad needed :', pad_needed)
		pad_bytes = get_bytes(pad_needed)
		print('pad bytes :', pad_bytes)
		pad_b10 = bytes_to_b10(pad_bytes)
		print('pad b10 :', pad_b10)
		text_ascii = get_ascii(text)
		print('text ascii :', text_ascii)
		encrypted_text = encrypt_text(text_ascii, pad_b10)
		print('encrypted text :', encrypted_text)
		binary_encrypted_text = int_to_binary(encrypted_text)
		print('binary encrypted text :', binary_encrypted_text)
		original_pad = pad_path
		prefix_file = open(pad_path[:-1]+'p', 'r')
		prefix = prefix_file.read()
		prefix_file.close()
		suffix_file = open(pad_path[:-1]+'s', 'r')
		suffix = suffix_file.read()
		suffix_file.close()
		pad_path = pad_path[:-1]+'t'
		pad_path = pad_path.split('/')
		writer = open(pad_path[0]+'-'+pad_path[1]+'-'+pad_path[2], 'w')
		writer.write(str(prefix)+str(''.join(binary_encrypted_text))+str(suffix))
		writer.close()
		subprocess.call(['shred', '-u', original_pad], shell = False)
	else:
		exit('The message can not fit in the pad')


def get_encrypted_text(prefix, text, suffix):
	''' (String, String, String) -> String

	get_encrypted_text('Bonjour', 'Bonjour comment allez-vous aujourd'hui', 'aujourd'hui')
	>>> ' comment allez-vous '
	'''
	return text[len(prefix):-len(suffix)]


def decrypt(text, pad):
	''' (list of int, list of int) -> String

	decrypt()
	>>>
	'''
	return ''.join(chr((text[i]-pad[i])%256) for i in range(len(text)))

def receive(args):
	''' () -> NoneType

	receive(args)
	>>>
	'''
	if args.transmission == None:
		exit('Transmission is not part of the input, now exiting ...')
	else :
		directory_path = args.transmission[:-4]
		directory_path = directory_path.split('-')
		directory_path = directory_path[0]+'/'+directory_path[1]+'/'
		pad_number = args.transmission.split('-')[2][:-1]
		file_prefix = open(directory_path+pad_number+'p', 'r')
		prefix_key = file_prefix.read()
		file_prefix.close()
		file_pad = open(directory_path+pad_number+'c', 'r')
		pad_key = file_pad.read()
		file_pad.close()
		file_suffix = open(directory_path+pad_number+'s', 'r')
		suffix_key = file_suffix.read()
		file_suffix.close()
		transmission_file = open(args.transmission, 'r')
		encrypted_text = transmission_file.read()
		transmission_file.close()
		encrypted_text = get_encrypted_text(prefix_key, encrypted_text, suffix_key)
		pad_key = get_pad_needed(encrypted_text, pad_key)
		text_bytes = get_bytes(encrypted_text)
		pad_bytes = get_bytes(pad_key)
		text_b10 = bytes_to_b10(text_bytes)
		pad_b10 = bytes_to_b10(pad_bytes)
		text = decrypt(text_b10, pad_b10)
		writer = open(args.transmission[:-1]+'m', 'w')
		writer.write(text)
		writer.close()
		subprocess.call(['shred', '-u', args.transmission], shell = False)
		subprocess.call(['shred', '-u', directory_path+pad_number+'c'], shell = False)

def todo():
	''' (NoneType) -> NoneType

	todo()
	>>>
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', dest = 'directory', required = True)
	parser.add_argument('--transmission', dest = 'transmission')
	parser.add_argument('-g', dest = 'generate', action = 'store_true')
	parser.add_argument('-s', dest = 'send', action = 'store_true')
	parser.add_argument('-f', dest = 'file')
	parser.add_argument('-t', dest = 'text')
	parser.add_argument('-r', dest = 'receive', action = 'store_true')
	args = parser.parse_args()
	if args.send != False:
		send(args)
	elif args.receive != False:
		receive(args)
	else:
		generate(args.directory)

if __name__ == "__main__":
	#check_interface()
	todo()