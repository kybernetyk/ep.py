#!/usr/bin/env python

# ep.py - a command line client for epguides.com
#
# Version 0.1a - (2011-01-02)
#
# licensed under GLP3 (because I have terminal RMS)
# see http://www.gnu.org/licenses/gpl-3.0.txt
#
# (c) Jaroslaw Szpilewski 2011
# http://nntp.pl

import urllib2
import re
import pprint
import sys
import time
import datetime

show_name = "howimetyourmother"

def retrieve_html_eplist ():
	resp = urllib2.urlopen("http://epguides.com/" + show_name);
	html = resp.read();
	
	start_pos = html.find('<pre>');
	stop_pos = html.find('</pre>');
	
	html = html[start_pos:stop_pos]
	
	return html.splitlines();

def get_episodes ():
	ep_list = retrieve_html_eplist();
	episodes  = [ ];
	for line in ep_list:
		if ('&bull' in line):
			continue;
		tmpline = re.sub('[ \t\n\r:]+', ' ', line); 
		columns = tmpline.split();

		if len(columns) < 4:
			continue;
		
		if not columns[0].isdigit():
			continue;

		epnum = columns[1];
		epdate = columns[3];
		if ('<a' in epdate):
			epdate = columns[2]

		raw_title = line 
		start_pos = raw_title.find("'>") + len("'>");
		stop_pos = raw_title.find("</a>");
		eptitle = raw_title[start_pos:stop_pos];
		episode = { 'epnum' : epnum,
								'airdate' : epdate,
								'title' : eptitle
							};
		episodes.append (episode);
	return episodes;

def filter_unaired (eplist):
	ret = [];
	now = datetime.datetime.now();

	time_format = "%d/%b/%y";
	for ep in eplist:
		airdate = ep['airdate'];
		if airdate.lower() == 'unaired':
			ret.append(ep);
			continue;

		then = datetime.datetime.fromtimestamp(time.mktime(time.strptime(airdate, time_format)))
		
		delta = now - then;
		if delta.days <= 0:
			ret.append(ep);
	return ret;

def main():
	global show_name
	if len(sys.argv) <= 1:
		print "syntax: %s [-a] <showname>\n\t-a = show all episodes. (default = show unaired)" % (sys.argv[0]);
		return;

	show_name = sys.argv[1];

	mode = 'unaired';
	
	if '-a' == sys.argv[1]:
		show_name = sys.argv[2];
		mode = 'all';

	show_name = re.sub(r'\s', '', show_name.lower())

	try:
		episodes = get_episodes();
	except urllib2.HTTPError as theerr:
		ecode = theerr.getcode();
		if ecode == 404:
			print "Error retrieving episode list!\n\tServer returned 404 - check the show's name!\n\tShow years has to be appended with an underscore _. Ex: v_2009 doctorwho_2005";
		else:
			print "epguides.com returned error code: " + str(ecode);
		return;
#	else:
#		print "error retrieving episode list."
#		return;
	
	if mode == 'unaired':
		episodes = filter_unaired(episodes);

	print "Showing %s episode list for '%s'" % (mode, sys.argv[1]);
	for ep in episodes:
		print ("ep #%s: airdate=%s title='%s'" % (ep['epnum'],ep['airdate'],ep['title']));

main();

