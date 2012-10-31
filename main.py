#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import cgi
import webapp2
import urllib
import json

from google.appengine.api import users
from google.appengine.ext import db

Location_url = 'http://localhost:8081'

# , encoding="latin-1"


class bookmark(db.Model):
  url = db.StringProperty()
  title = db.StringProperty()
  content = db.StringProperty(multiline=True)
  user = db.StringProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/html; charset=utf-8"
        self.response.out.write("""Welcome to <a href="">[trishmarks]</a> .""")
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("%s" % greeting)
            self.response.out.write("""<hr/>""")
            u = user.user_id();
            bookmarks = db.GqlQuery("SELECT * FROM bookmark WHERE user = :1 ", u )
            self.response.out.write(bookmarks.count())
            for bkm in bookmarks:
              self.response.out.write("""<a href="%s">%s</a> { <a href="delete?id=%s">delete</a> | <a href="read?u=%s" target="_blank">readability</a> }""" %
                                    ( urllib.unquote(bkm.url) , urllib.unquote(bkm.title) , bkm.key() , bkm.url  ) )
              cont = urllib.unquote( bkm.content )
              self.response.out.write('<blockquote>%s</blockquote>' % cont )
              self.response.out.write('<sppan>%s</span><br/>' % bkm.user )
              
        else:
            greeting = ("Please <a href=\"%s\">Login</a>" % (users.create_login_url("/")))
            self.response.out.write("%s" % greeting)
            self.response.out.write("""<hr/>""")
            self.response.out.write("""Please drag the bookmarklet link (This one -> <a href="">[Trishmark]</a>) to your bookmark toolbar.<br/>
After installing the bookmarklet you can use this by selecting part of the page and then clicking the bookmarklet.
Your page and selected text will be saved and no time will be wasted.<br>
This bookmarking site's USP is to keep out of your way as much as possible, but still be an invaluable assistant for the lang haul.""")
    
        y = '%u2014'
        self.response.out.write('%s' % y )

class SaveA(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.headers['Content-Type'] = "text/plain; charset=utf-8"
        if user:
          u = user.user_id();
          url = self.request.get('u')
          bm = bookmark()
          bm.url = url
          title = self.request.get('t')
          if( title == ""):
            bm.title = self.request.get('u')
          else:
            bm.title = title
          bm.content = self.request.get('c')
          bm.user = user.user_id()
          bm.put()
          
          response = json.dumps({'text':'success!'})
          self.response.out.write("function parseRequest(response){alert('Response: '+response.text);}")
          self.response.out.write('parseRequest('+response+')')
        else:
          QueryString = self.request.query_string
          url = users.create_login_url('/savepl?'+QueryString)
          self.response.out.write("window.open('"+Location_url+url+"','_self');")

class Save(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.headers['Content-Type'] = "text/plain; charset=utf-8"
        if user:
          u = user.user_id();
          url = self.request.get('u')
          bookmarks = db.GqlQuery("SELECT * FROM bookmark WHERE user = :1 AND url = :2", u , url )
          if(int(bookmarks.count()) > 0):
            QueryString = self.request.query_string
            url = Location_url +'/savea?'+QueryString
            url1 = Location_url +'/merge?'+QueryString
            self.response.out.write("""
u = "You have already bookmarked this site.\\nHowever if you wish, the new save can be merged with the old one.\\nWould you like to proceed?\\nHitting the cancel button will save the bookmark separately.";
function mergeRequest(){
yo = confirm(u);
if(yo){window.open('%s','_self');}else{var scr=document.createElement('script');scr.setAttribute('src','%s');document.getElementsByTagName('head')[0].appendChild(scr);}
}
mergeRequest();

""" % ( url1 , url ))
          else:
            bm = bookmark()
            bm.url = url
            title = self.request.get('t')
            if( title == ""):
              bm.title = self.request.get('u')
            else:
              bm.title = title
            bm.content = str(self.request.get('c'))
            bm.user = user.user_id()
            bm.put()
          
            response = json.dumps({'text':'success!'})
            self.response.out.write("function parseRequest(response){alert('Response: '+response.text);}")
            self.response.out.write('parseRequest('+response+')')
        else:
          QueryString = self.request.query_string
          url = users.create_login_url('/savepl?'+QueryString)
          self.response.out.write("window.open('"+Location_url+url+"','_self');")

# save post login
class SavePL(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
          bm = bookmark()
          bm.url = self.request.get('u')
          t = self.request.get('t')
          if( t == ""):
            bm.title = self.request.get('u')
          else:
            bm.title = t
          bm.content = self.request.get('c')
          bm.user = user.user_id()
          bm.put()
          self.redirect(str(self.request.get('u')))
        else:
          url = users.create_login_url(self.request.uri)
          self.response.out.write("window.open('"+Location_url+url+"','_self');")

class MergeForm(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      u = user.user_id()
      url = self.request.get('u')
      title = self.request.get('t')
      cc = ''
      bookmarks = db.GqlQuery("SELECT * FROM bookmark WHERE user = :1 AND url = :2", u , url )
      for bk in bookmarks:
        cc += bk.content
      cc += self.request.get('c')
      self.response.out.write("""<script type='text/javascript'>function getContent(){document.getElementById('my-textarea').value = document.getElementById('my-content').innerHTML;}</script><div id="my-content" contenteditable="true">%s</div><form id="form" action="/mergesave" onsubmit="return getContent()" method="post"><textarea id="my-textarea" name="content" style="display:none"></textarea><input type="hidden" name="title" value="%s"><input type="hidden" name="url" value="%s"><input type="submit" value="Save Merged Bookmark"/></form>""" % (cc,title,url))
    else:
      self.redirect(users.create_login_url(self.request.uri))

class MergeSave(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
          u = user.user_id()
          url = str(self.request.get('url'))
          content = str(self.request.get('content'))
          cc = ''
          title = str(self.request.get('title'))
          bookmarks = db.GqlQuery("SELECT * FROM bookmark WHERE user = :1 AND url = :2", u , url )
          for bk in bookmarks:
            title = bk.title
            key = bk.key()
            db.delete(key)
          bm = bookmark()
          bm.url = url
          bm.user = u
          bm.title = title
          bm .content = content
          bm.put()
          self.redirect(cgi.escape(url))
        else:
          self.redirect(users.create_login_url(self.request.uri))
            

     
class Delete(webapp2.RequestHandler):
    def get(self):
        key = self.request.get('id')
        db.delete(key)
        self.redirect('/')

class Read(webapp2.RequestHandler):
    def get(self):
        link = str('http://www.readability.com/read?url='+self.request.get('u') )
        self.redirect(link)

app = webapp2.WSGIApplication([('/', MainPage),
                              ('/save', Save),
                              ('/merge', MergeForm),
                              ('/savea', SaveA),
                              ('/savepl', SavePL),
                              ('/delete', Delete),
                              ('/mergesave', MergeSave),
                              ('/read', Read)],
                              debug=True)
