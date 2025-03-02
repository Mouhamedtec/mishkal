﻿#! /usr/bin/python
import sys
sys.path.append('lib');
import re
import string
import datetime
import getopt
import os
import pyarabic.araby as araby
import qalsadi.analex
					
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
AuthorName="Taha Zerrouki"
#Token_pattern=re.compile(u"([\w%s ]+)"%(u"".join(araby.TASHKEEL),),re.UNICODE);
Clause_pattern=re.compile(u"([\w%s\s]+)"%(u"".join(araby.TASHKEEL),),re.UNICODE);

#Token_pattern=re.compile(u"([^\w]+)",re.UNICODE);
# Token_pattern=re.compile(u"([^\w%s\s])+"%(u"".join(araby.TASHKEEL),),re.UNICODE);

def phraseSplit(text):
	"""
	Split Text into clauses
	@param text: input text;
	@type text: unicode;
	@return: list of clauses
	@rtype: list of unicode
	"""
	if text:
		list_phrase=Clause_pattern.split(text);
		if list_phrase:
			j=-1;
			newlist=[];
			for ph in list_phrase:
				if not Clause_pattern.match(ph):
					#is pounctuation or symboles
					#print 'not match', ph.encode('utf8');
					if j<0:
						# the symbols are in the begining
						newlist.append(ph);
						j=0;
					else:
						# the symbols are after a phrases
						newlist[j]+=ph;
				else:
					newlist.append(ph);
					j+=1;
		return newlist;
	return [];
def usage():
# "Display usage options"
	print "(C) CopyLeft 2009, %s"%AuthorName
	print "Usage: %s -f filename [OPTIONS]" % scriptname
#"Display usage options"
	print "\t[-h | --help]\t\toutputs this usage message"
	print "\t[-v | --version]\tprogram version"
	print "\t[-l | --limit]\t vocalize only a limited number of line"
	print "\t[-s | --syntax]\t  disable syntaxic analysis"
	print "\t[-m | --semantic]\t disable semantic analysis"
	print "\t[-c | --compare]\t compare the vocalized text with the program output"
	print "\t[-t | --stat]\t disable statistic tashkeel"
	print "\t[-i | --ignore]\t ignore the last Mark on output words."	
	print "\t[-f | --file= filename]\tinput file to %s"%scriptname
	print "\r\nThis program is licensed under the GPL License\n"

def grabargs():
#  "Grab command-line arguments"
	fname = ''
	suggestion=False;
	ignore= False;
	limit=False; 
	compare = False;
	disableSyntax = False;
	disableSemantic = False;
	disableStatistic=  False;
	if not sys.argv[1:]:
		usage()
		sys.exit(0)
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hVtcismv:f:l:",
                               ["help", "version","stat","compare", "syntax","semantic", "ignore","limit=", "file="],)
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for o, val in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit(0)
		if o in ("-V", "--version"):
			print scriptversion
			sys.exit(0)
		if o in ("-s", "--syntax"):
			disableSyntax = True
		if o in ("-m", "--semantic"):
			disableSemantic = True

		if o in ("-i", "--ignore"):
			ignore = True;
		if o in ("-c", "--compare"):
			compare = True;
		if o in ("-t", "--stat"):
			disableStatistic = True;
			
			
		if o in ("-l", "--limit"):
			try: limit = int(val);
			except: limit=0;
		if o in ("-s", "--seg"):
			suggestion = True			
		if o in ("-f", "--file"):
			fname = val

	return (fname, disableSyntax, disableSemantic, disableStatistic, ignore, limit ,compare)

if __name__ == '__main__':
	filename, disableSyntax, disableSemantic, disableStat, ignore, limit, compare =grabargs()
	#filename="samples/randomtext.txt"	
	try:
		myfile=open(filename)
	except:
		print " Can't Open the given File ", filename;

	counter=1;
	if not limit : 
		limit=	100000000
	nolimit = False;
	correct=0;
	total=0;
	analyzer=qalsadi.analex.analex();
	line=(myfile.readline()).decode('utf8');
	while line and (nolimit or counter<=limit):
		phrases=analyzer.check_text(line);
		print u"\t".join(['#',str(counter),line]).encode('utf8');
		print phrases;
		#get the next line
		line=(myfile.readline()).decode('utf8');
		counter+=1;
	#print correct, total, round(correct*100.00/total,2)