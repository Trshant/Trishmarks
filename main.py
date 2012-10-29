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

class bookmark(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  url = db.StringProperty()
  title = db.StringProperty()
  content = db.StringProperty(multiline=True)
  user = db.StringProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("""Welcome to <a href="">[trishmarks]</a> .""")
        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
            self.response.out.write("%s" % greeting)
        self.response.out.write("""<hr/>""")
        bookmarks = bookmark.gql("LIMIT 100")
        for bkm in bookmarks:
          self.response.out.write("""<a href="%s">%s</a> { <a href="delete?id=%s">delete</a> | <a href="read?u=%s" target="_blank">readability</a> }""" %
                                  ( urllib.unquote(bkm.url) , urllib.unquote(bkm.title) , bkm.key() , bkm.url  ) )
          cont = urllib.unquote( bkm.content )
          self.response.out.write('<blockquote>%s</blockquote>' % cont )
          self.response.out.write('<sppan>%s</span><br/>' % bkm.user )
        y = '%u2014'
        self.response.out.write('%s' % y )

class Save(webapp2.RequestHandler):
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
          self.response.headers['Content-Type'] = "text/plain; charset=utf-8"
          response = json.dumps({'text':'success!'})
          self.response.out.write("function parseRequest(response){alert('Response: '+response.text);}")
          self.response.out.write('parseRequest('+response+')')
        else:
          QueryString = self.request.query_string
          url = users.create_login_url('/savepl?'+QueryString)
          self.response.out.write("window.open('http://localhost:8080"+url+"','_self');")

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
          self.response.out.write("window.open('http://localhost:8080"+url+"','_self');")


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
                              ('/savepl', SavePL),
                              ('/delete', Delete),
                              ('/read', Read)],
                              debug=True)
