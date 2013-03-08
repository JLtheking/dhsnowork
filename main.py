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

from google.appengine.ext import db
from google.appengine.api import users

class Group(db.Model):
  #basic info of group
  name = db.StringProperty()
  subject = db.StringProperty()
  description = db.StringProperty()
  memberCount = db.IntegerProperty()
  
  # Group affiliation
  members = db.ListProperty(db.Key)
  
  @property
  def members(self):
    return Member.gql("WHERE groups = :1", self.key())

class Member(db.Model):
    #id of user according to dhs.sg accountname
    username = user.User()
    
    #basic info of member
    fullName = db.StringProperty()
    classId = db.StringProperty()
    
    # Group affiliation
    groups = db.ListProperty(db.Key)
    
    @property
    def groups(self):
        return Group.gql("WHERE members = :1", self.key())
    
class MemberGroup(db.Model):
    member = db.ReferenceProperty(Member,required=True,collection_name='groups')
    group = db.ReferenceProperty(Group,required=True,collection_name='members')
    ##to add someone to a group:
    #mary = Contact.gql("name = 'Mary'").get()
    #google = Company.gql("name = 'Google'").get()
    #ContactCompany(contact=mary,
    #               company=google,
    #               title='Engineer').put()
    

class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()

    if user:
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write('Hello, ' + user.nickname())
    else:
      self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)