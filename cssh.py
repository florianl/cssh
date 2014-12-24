#!/usr/bin/env python

import fileinput
import string
import os
import signal
import sys
import curses

hosts = list()

def parser():
	for line in fileinput.input(os.path.expanduser('~/.ssh/config')):
		if not line:
			continue
		else:
			s = line.strip()
			if s.lower().startswith("host"):
				if s.lower().startswith("hostname"):
					continue
				h = s.split()
				hosts.append(h[1])
			else:
				continue
	fileinput.close()

def printlist(scr):
	i = 2
	if hosts == []:
		parser()

	j = scr.getmaxyx()

	for item in hosts:
		line = ""
		listid = hosts.index(item)
		if j[1] > 79:
			if i%2 == 1:
				scr.addstr(i-1, 43, str(listid))
				scr.addstr(i-1, 46, "- " +item)
			else:
				scr.addstr(i, 3, str(listid))
				scr.addstr(i, 6, "- " +item)
		else:
			scr.addstr(i, 3, str(listid))
			scr.addstr(i, 6, "- " +item)
		i=i+1
	i = i+2
	scr.addstr(i,6, "# ")
	return i

# Handle CTRL+C
def signal_handler(signal, frame):
	curses.nocbreak()
	curses.echo()
	curses.endwin()
	os.system("clear")
	sys.exit(0)

def ctrlExit():
	curses.nocbreak()
	curses.echo()
	curses.endwin()
	os.system("clear")
	sys.exit(0)

def connect2host(n, line):
	nr = int(n)
	if len(hosts) == 0:
		scr.clear()
		scr.addstr(3,3, "# ")
		scr.addstr(4, 5, "There are no hosts", curses.A_BOLD)
		scr.border(0)
		scr.refresh()
		return
	if nr <= len(hosts):
		curses.endwin()
		print "connecting ..."
		host = hosts[nr]
		cmd = 'ssh ' + host + ' -t "screen -raAd || screen"'
		os.system(cmd)
		scr.clear()
		inputline = printlist(scr)
	else :
		scr.clear()
		inputline = printlist(scr)
		scr.addstr(inputline+1, 5, str(nr) +" is an unknown host", curses.A_BOLD)
	scr.border(0)
	scr.refresh()

os.system("clear")
signal.signal(signal.SIGINT, signal_handler)
scr = curses.initscr()
curses.cbreak()
curses.echo()
inputline = printlist(scr)
scr.border(0)
scr.refresh()
y, x = scr.getmaxyx()
while True:
	try:
		n = scr.getstr(inputline,8, 7)
	except EOFError:
		ctrlExit()
	if n.isdigit():
		connect2host(n, inputline)
	elif n.lower() == 'q':
		ctrlExit()
	elif n.lower() == 'exit':
		ctrlExit()

	resized = curses.is_term_resized(y, x)
	if resized is True:
		y, x = scr.getmaxyx()
		scr.clear()
		curses.resizeterm(y, x)
		inputline = printlist(scr)
		scr.border(0)
		scr.refresh()
