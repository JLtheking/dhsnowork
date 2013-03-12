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
import urllib
import webapp2
import jinja2
import os

from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Group(db.Model):
  #basic info of group
  name = db.StringProperty()
  subject = db.StringProperty()
  description = db.StringProperty()
  memberCount = db.IntegerProperty(default=0)
  
  # Group affiliation
  parents = db.ListProperty(db.Key)

class Member(db.Model):
    #id of user according to dhs.sg accountname
    username = db.StringProperty()
    
    #basic info of member
    fullName = db.StringProperty()
    classId = db.StringProperty()
    
    # Group affiliation
    parents = db.ListProperty(db.Key)
    
class MemberGroup(db.Model):
    member = db.ReferenceProperty(Member,
                                   required=True,
                                   collection_name='groups')
    group = db.ReferenceProperty(Group,
                                   required=True,
                                   collection_name='members')
    title = db.StringProperty()
    
    ##to add someone to a group:
    #mary = Contact.gql("name = 'Mary'").get()
    #google = Company.gql("name = 'Google'").get()
    #ContactCompany(contact=mary,
    #               company=google,
    #               title='Engineer').put()
    

class MainPage(webapp2.RequestHandler):
  def get(self):
    
    
    
    #get current user //currentUser.nickname() returns email
    currentUser = users.get_current_user()
    
    if currentUser:
      logio = users.create_logout_url(self.request.uri)
      logio_linktext = 'Logout'
    else:
      self.redirect(users.create_login_url(self.request.uri))
      logio = users.create_login_url(self.request.uri)
      logio_linktext = 'Login'

    #these values are what gets subbed into the html through jinja2
    template_values = {
      'logio': logio,
      'logio_linktext': logio_linktext,
      'currentUserNickname': currentUser.nickname()
    }
    
    #locate and render the template
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)