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
        self.response.out.write("""Welcome to <a href="javascript:var%20obj;function%20ProcessXML(url){if(window.XMLHttpRequest){obj=new%20XMLHttpRequest();obj.onreadystatechange=processChange;obj.open('GET',url,true);obj.send(null)}else%20if(window.ActiveXObject){obj=new%20ActiveXObject('Microsoft.XMLHTTP');if(obj){obj.onreadystatechange=processChange;obj.open('GET',url,true);obj.send()}}else{alert('Your%20browser%20does%20not%20support%20AJAX')}}function%20processChange(){if(httpRequest.readyState===4){if(httpRequest.status===200){alert(httpRequest.responseText)}else{alert('There%20was%20a%20problem%20with%20the%20request.')}}}Q='';ss='http://trshant-bookmarks.appspot.com/save?c=';x=document;y=window;if(x.selection){Q=x.selection.createRange().text}else%20if(y.getSelection){Q=y.getSelection()}else%20if(x.getSelection){Q=x.getSelection()}for(i=0,l=Q.rangeCount;i<l;i++){ss+=escape(Q.getRangeAt(i).toString())+'<br/>'}ss+='&u='+encodeURI(location.href)+'&t='+escape(document.title);ProcessXML(ss)">[trishmarks]</a> .
            <hr/>""")
        bookmarks = bookmark.gql("LIMIT 100")
        for bkm in bookmarks:
          self.response.out.write("""<a href="%s">%s</a> { <a href="delete?id=%s">delete</a> | <a href="read?u=%s" target="_blank">readability</a> }""" %
                                  ( urllib.unquote(bkm.url) , urllib.unquote(bkm.title) , bkm.key() , bkm.url  ) )
          cont = urllib.unquote( bkm.content )
          self.response.out.write('<blockquote>%s</blockquote>' % cont )

class Save(webapp2.RequestHandler):
    def get(self):
        bm = bookmark()
        bm.url = self.request.get('u')
        t = self.request.get('t')
        if( t == ""):
          bm.title = self.request.get('u')
        else:
          bm.title = t
        bm.content = self.request.get('c')
        bm.user = "trshant"
        bm.put()
        self.response.out.write('success!')

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
                              ('/delete', Delete),
                              ('/read', Read)],
                              debug=True)
