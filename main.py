# -*- coding:utf-8 -*-

import os
from os import walk

def check_interface():
	for root, directories, files in walk("/sys/class/net/"):
		for directory in directories:
			file = open("/sys/class/net/"+directory+"/operstate", 'r')
			for state in file:
				if state == 'up\n':
					exit('Interface is up, now exiting ...')
	

if __name__ == "__main__":
	check_interface()