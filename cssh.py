#!/usr/bin/env python

import fileinput
import string
import os
import signal
import sys
import curses

hosts = list()

def parser():
	for line in fileinput.input("~/.ssh/config"):
		if not line:
			continue
		else:
			if line.startswith("HOST"):
				s = line.strip()
				s = line.strip("HOST")
				s = s.strip()
				hosts.append(s)
			else:
				continue
	fileinput.close()

def printlist():
	if hosts == []:
		parser()

	for item in hosts:
		listid = hosts.index(item)
		print listid, "\033[34m" + item + "\033[0m"

# Handle CTRL+C
def signal_handler(signal, frame):
	os.system("clear")
	sys.exit(0)

def go2exit():
	os.system("clear")
	sys.exit(0)

def catchedNr(n):
	nr = int(n)
	host = hosts[nr]
	cmd = 'ssh ' + host + ' -t "screen -raAd"'
	os.system(cmd)

msg = ""
os.system("clear")
signal.signal(signal.SIGINT, signal_handler)
while True:
	printlist()
	print "\033[91m" + msg + "\033[0m"
	try:
		n = raw_input("# ")
	except EOFError:	# capture CTRL+D
		go2exit()

	if n.startswith("exit"):
		go2exit()
	elif n in hosts:
		cmd = 'ssh ' + n + ' -t "screen -raAd"'
		msg = ""
		os.system(cmd)
		os.system("clear")
	elif n.isdigit():
		catchedNr(n)
		msg = ""
		os.system("clear")
	else:
		os.system("clear")
		msg = "can't handle: " + n
