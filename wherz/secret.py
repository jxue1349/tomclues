#!/usr/bin/env python
#
# Copyright 2015 WhereLast Inc.
#
###
################ library functions ###############
###
import random
import string
import hashlib
import hmac

import os
import jinja2
import webapp2
import urllib2

# third party lib
from google.appengine.ext import vendor
vendor.add('lib')
from autocorrect import spell

template_dir = os.path.join(os.path.dirname(__file__), 'src')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


def secret():
	return 'morek8913%@&$jgmew<jfemw'

# Password hash function 
def make_salt():
	return "".join(random.choice(string.letters) for x in xrange(5))
def make_pw_hash(name, pw, salt=None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(secret.secret() + name + pw + salt).hexdigest()
	return '%s|%s' % (h, salt)
def valid_pw(name, pw, h):
	salt = h.split("|")[1]
	return h == make_pw_hash(name, pw, salt)
def users_key(group = 'default'):
	return db.Key.from_path('users', group)
def make_secure_val(val):
	return '%s|%s' % (val, hmac.new(secret.secret(), val).hexdigest())
def check_secure_val(secure_val):
	val = secure_val.split('|')[0]
	if secure_val == make_secure_val(val):
		return val

# Render page handler 
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

