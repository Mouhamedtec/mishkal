#!/usr/bin/python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        adawaty
# Purpose:    web interface tools for manipulating arabic texts.
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------

"""
The original web interface is friom webQamoos,

Copyright © 2009, Muayyad Alsadi <alsadi@ojuba.org>
    Released under terms of Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://waqf.ojuba.org/license"

"""
import sys

import os
import os.path
import re
from glob import glob


sys.path.append('mishkal/');
sys.path.append('mishkal/lib/');
sys.path.append('lib');
sys.path.append('lib/web');
from okasha2.baseWebApp import *
from okasha2.utils import fromFs, toFs
import core.adaat
# import core.myrepr
import datetime

header=u"""
<div style='text-align:left;vertical-align:middle; display:table-cell;'>

     <a href="/mishkal/index">الرئيسية</a>&nbsp;&nbsp;
    <a href="/mishkal/doc">توثيق</a>&nbsp;&nbsp;
      <a href="/mishkal/link">روابط</a>&nbsp;&nbsp;
<a href="/mishkal/download">تحميل</a>&nbsp;&nbsp;
	<a href="/mishkal/projects">مشاريع</a>&nbsp;&nbsp;
      <a href="/mishkal/contact">اتصل بنا</a>&nbsp;&nbsp;
</div>
<hr/>
"""


footer=u"""
<hr class="footer"/>
  <div id="footer">
    <a href="/mishkal/contact">للاتصال</a>&nbsp;
    &nbsp;بدعم من &nbsp;&nbsp; <a href="http://www.arabeyes.org">arabeyes.org</a>
	<a href="http://blog.tahadz.com">مدونتي</a>
	</div>

"""

MyJsonHeaders={
	"Access-Control-Allow-Methods":		"GET, POST, OPTIONS",
	"Access-Control-Allow-Credentials": "true",
	"Access-Control-Allow-Origin": 		"*",
	"Access-Control-Allow-Headers": 	"Content-Type, *",
}

#used in local
#comment it on server
# header=re.sub("/mishkal/",'', header);
# footer=re.sub("/mishkal/",'', footer);
class webApp(baseWebApp):

	def __init__(self, *args, **kw):
		baseWebApp.__init__(self,*args, **kw)
		# self.myRepr = core.myrepr.MyRepr();


	def _root(self, rq, *args):
		raise redirectException(rq.script+'/main')

	@expose(percentTemplate,["main.html"])
	def main(self, rq, *args):
		return {
	  'title':u'أدوات',
	  'script':rq.script,
	  'DefaultText':core.adaat.randomText(),
	  'ResultText':u"السلام عليكم",
		'header':header,
		"footer":footer,	  
#      'mode':self.mode, 'version':'0.1.0'
		}
	@expose(percentTemplate,["main.html"])
	def index(self, rq, *args):
		return {
	  'title':u'مشكال لتشكيل النصوص',
	  'script':rq.script,
	  'DefaultText':core.adaat.randomText(),
	  'ResultText':u"السلام عليكم",
		'header':header,
		"footer":footer,	  
#      'mode':self.mode, 'version':'0.1.0'
		}
	@expose(percentTemplate,["body_help.html"])
	def help(self, rq, *args):
		return {
		}
	@expose(jsonDumps, headers=MyJsonHeaders)
	def ajaxGet(self, rq,  *args):
		"""
		this is an example of using ajax/json
		to test it visit http://localhost:8080/ajaxGet"
		"""
		text=rq.q.getfirst('text','ZerroukiTAha').decode('utf-8')
		action=rq.q.getfirst('action','DoNothing').decode('utf-8')
		order=rq.q.getfirst('order','0').decode('utf-8')
		options={};
		options['lastmark']=rq.q.getfirst('lastmark','0').decode('utf-8')		
		#print order.encode('utf8');
		self.writelog(text,action);
		#Handle contribute cases
		if action=="Contribute":
			return {'result':u"شكرا جزيلا على مساهمتك."}
		resulttext=core.adaat.DoAction(text,action, options)
		# self.writelog(repr(resulttext),"ResultText");
		# we choose to avoid logging results
		# self.writelog(resulttext,"ResultText");		
		return {'result':resulttext, 'order':order}

	@expose(percentTemplate,["doc.html"])
	def doc(self, rq, *args):
		return {
		'script':rq.script,
		'header':header,
		"footer":footer,
		}
	@expose(percentTemplate,["download.html"])
	def download(self, rq, *args):
		return {
		'script':rq.script,
		'header':header,
		"footer":footer,
		}
	@expose(percentTemplate,["contact.html"])
	def contact(self, rq, *args):
		return {
		'script':rq.script,
		'header':header,
		"footer":footer,
		}
	@expose(percentTemplate,["link.html"])
	def link(self, rq, *args):
		return {
		'script':rq.script,
		'header':header,
		"footer":footer,
		}
	@expose(percentTemplate,["projects.html"])
	def projects(self, rq, *args):
		return {
		'script':rq.script,
		'header':header,
		"footer":footer,
		}
	@expose(percentTemplate,["log.html"])
	def log(self, rq, *args):
		return {
		'script':rq.script,
		'header':header,
		"footer":footer,
		}
	@expose(percentTemplate,["whoisqutrub.html"])
	def whoisqutrub(self, rq, *args):
		return {
		'script':rq.script,
		'header':header,
		"footer":footer,
		}

	def writelog(self,text,action):
		"""
		@param text: an object to be logged
		@type text: object
		"""
		timelog=datetime.datetime.now().strftime("%Y-%m-%d %I:%M");
		textlog=u"\t".join([timelog,action, text]);
		self._logger.info(textlog);

