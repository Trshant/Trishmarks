#!/usr/bin/env python
#
# Copyright 2007 Trshant Bhat.
#
# 
# This file is the main file for my app running on GAE called trishmarks.
# 
#
# 
#


import cgi
import webapp2
import urllib
import json
import jinja2
import os
import datetime

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

Location_url = 'http://trshant-bookmarks.appspot.com' ## 'http://localhost:8081' ## 'http://trshant-bookmarks.appspot.com'

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def unquote_u(source):
  result = source
  if '%u' in result:
    result = result.replace('%u','\\u').decode('unicode_escape')
  result = urllib.unquote(result)
  return result


class bookmark(db.Model):
  url = db.StringProperty()
  title = db.StringProperty()
  content = db.TextProperty()  ##db.StringProperty(multiline=True)
  user = db.StringProperty()
  date_save = db.DateProperty()


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/html; charset=utf-8"
        
        user = users.get_current_user()
        if user:
            u = user.user_id();
            bookmarks_query = db.GqlQuery("SELECT * FROM bookmark WHERE user = :1 ", u )
            bookmarks = bookmarks_query
            content = "";
            
            template_values = {
				'username' : user.nickname() ,
				'logout_url' : users.create_logout_url("/") ,
				'content' : bookmarks ,
				'loc_url': Location_url ,
			}
			
            template = jinja_environment.get_template('logged_in_template.html')
            self.response.out.write(template.render(template_values))
			
            ##path = os.path.join(os.path.dirname(__file__), 'logged_in_template.html')
            ##self.response.out.write(template.render(path, template_values))
			
              
        else:
		
            template_values = {
                'loc_url' : Location_url ,
                'login_url' : users.create_login_url("/") ,
			}
            
            template = jinja_environment.get_template('landing_page.html')
            self.response.out.write(template.render(template_values))
			
            ##path = os.path.join(os.path.dirname(__file__), 'landing_page.html')
            ##self.response.out.write(template.render(path, template_values))
			
			
            
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
          bm.date_save = datetime.datetime.now().date()
          bm.put()
          
          response = json.dumps({'text':'success!'})
          self.response.out.write("function parseRequest(response){alert('Response: '+response.text);}")
          self.response.out.write('parseRequest('+response+')')
        else:
          QueryString = self.request.query_string
          url = users.create_login_url('/savepl?'+QueryString)
          self.response.out.write("window.open('"+url+"','_self');")

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
if(yo){window.open("%s",'_self');}
else{
var scr=document.createElement('script');
scr.setAttribute('src',"%s");
document.getElementsByTagName('head')[0].appendChild(scr);
}
}
mergeRequest();

""" % ( url1 , url ))
          else:
            bm = bookmark()
            bm.url = url
            title = safe_unicode(unquote_u(self.request.get('t')))
            if( title == ""):
              bm.title = self.request.get('u')
            else:
              bm.title = title
            bm.content = safe_unicode(unquote_u(self.request.get('c'))) ##str(self.request.get('c'))
            bm.user = user.user_id()
            bm.date_save = datetime.datetime.now().date()

            bm.put()
          
            response = json.dumps({'text':'success!'})
            self.response.out.write("function parseRequest(response){alert('Response: '+response.text);}")
            self.response.out.write('parseRequest('+response+')')
        else:
          QueryString = self.request.query_string
          url = users.create_login_url('/savepl?'+QueryString)
          self.response.out.write("window.open('"+url+"','_self');")

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
          bm.date_save = datetime.datetime.now().date()
          bm.put()
          self.redirect(str(self.request.get('u')))
        else:
            self.redirect( users.create_login_url(self.request.uri) )
            url = users.create_login_url(self.request.uri)
            self.response.out.write("window.open('"+url+"','_self');")

class MergeForm(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
        u = user.user_id()
        url = self.request.get('u')
        title = self.request.get('t')
        mode = self.request.get('m')
        bid = self.request.get('id')
        cc = ''
        global temple_values
        
        bookmarks = db.GqlQuery("SELECT * FROM bookmark WHERE user = :1 AND url = :2", u , url )
        if(bid):
            bookmarks = bookmarks =db.get(bid)
            cc   += bookmarks.content
            url   = bookmarks.url
            title = bookmarks.title
			
            button_text = '&nbsp;Save&nbsp;?&nbsp;'
			
        else:
            for bk in bookmarks:
                cc += bk.content
            button_text = '&nbsp;Merge&nbsp;?&nbsp;'

        nick = user.nickname()
        logout_url = users.create_logout_url("/")
        temple_values = {
		    'title' : title ,
		    'mode' : mode ,
		    'url' : url ,
            'username' : nick ,
            'logout_url' : logout_url ,
            'loc_url': Location_url ,
            'content' : cc,
            'button_text' : button_text ,
	    }
		
        templater = jinja_environment.get_template('edit.html')
        self.response.out.write(templater.render(temple_values))
	  
    else:
        self.redirect(users.create_login_url(self.request.uri))

class MergeSave(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
          u = user.user_id()
          url = str(self.request.get('url'))
          mode = str(self.request.get('mode'))
          content = safe_unicode(unquote_u(self.request.get('content')))
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
          bm.content = content
          bm.date_save = datetime.datetime.now().date()
          bm.put()
          if(mode == "1"):
            self.redirect(cgi.escape(Location_url))
          else:
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
