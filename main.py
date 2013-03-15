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
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape = True
)

### PAGES
class MainPage(webapp2.RequestHandler):
  def render_page(self,currentUserNickname, groups):
        template_values = {
            'currentUserNickname': currentUserNickname,
            'groups': groups,
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))
  
  def get(self):
    
    #receive linkage to current user
    currentUser = users.get_current_user()
    
    #default template values
    currentUserNickname = "limahseng@dhs.sg"
    
    #user handlers
    if not currentUser:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      currentUserNickname = currentUser.nickname()
      groups = db.GqlQuery("SELECT * FROM Group")
    
    self.render_page(currentUserNickname, groups)
    
  def post(self):
    pass

### DATASTORE ENTITIES
class Group(db.Model):
  #basic info of group
  name = db.StringProperty(required = True)
  subject = db.StringProperty()
  description = db.TextProperty()
  memberCount = db.IntegerProperty(default=1)
  admin = db.StringProperty()
  
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
    
class Feedback(db.Model):
    user = db.StringProperty(required = True)
    text = db.TextProperty(required = True)
    rating = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)



### HANDLERS
class SubmitFeedbackHandler(webapp2.RequestHandler):
    def post(self):
        currentUser = users.get_current_user()
        
        user = currentUser.nickname()
        text = self.request.get("textarea")
        rating = int(self.request.get("slider"))
        
        feedback = Feedback(user = user, text = text, rating = rating)
        feedback.put()
        
        self.redirect("/")
        
class NewGroupHandler(webapp2.RequestHandler):
    def post(self):
        currentUser = users.get_current_user()
        
        admin = currentUser.nickname()
        name = self.request.get("groupname")
        subject = self.request.get("subject")
        description = self.request.get("description")
        
        group = Group(name = name, subject = subject, description = description, admin = admin)
        group.put()

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/submitFeedback', SubmitFeedbackHandler),
                               ('/newgroup', NewGroupHandler)],
                              debug=True)