#!/usr/bin/env python
#
# Copyright 2015 WhereLast Inc.
#
###
################# Login / registration page handler ####################
###
from library import *
from database import User


# login/sign up page handler
class LoginHandler(Handler):
	def render_front(self, rtype="signin", useremail="", pwd="", cpwd="", error=""):
		self.render("login.html", rtype=rtype, useremail=useremail, pwd=pwd, cpwd=cpwd, error=error)

	def get(self):
		self.render_front();

	def set_secure_cookie(self, name, val):
		cookie_val = make_secure_val(val)
		self.response.headers.add_header(
			'Set-Cookie',
			'%s=%s; Path=/' % (name, cookie_val))

	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		return cookie_val and check_secure_val(cookie_val)

	def login(self, user):
		self.set_secure_cookie('user_id', str(user.key().id()))

	def logout(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie('user_id')
		self.user = uid and User.by_id(int(uid))

	def post(self):
		signin = self.request.get("signin-button")
		signup = self.request.get("signup-button")
		email = self.request.get("email")
		pwd = self.request.get("pwd")

		error = ""
		if not valid_email(email):
			error = "invalid email address"
		if not valid_password(pwd):
			if signin:
				error = "invalid password"
			elif signup:
				error = "invalid password. Password should be 3-20 characters including numbers, letters and !@#$%^&*_"

		if signin: 
			if error:
				self.render_front(rtype="signin", useremail=email, pwd=pwd, error=error)
			else:
				# next step is to check user name and password is matching database
				# if yes, redirect to user.html
				# if not, re-render the login page with error message
				u = User.login(email, pwd)

				
				if u == 1:
					error = "account is not existing, try signup"
					self.render_front(rtype="signup", useremail=email, pwd=pwd, error=error)
				elif not u:
					error = "invalid password"
					self.render_front(rtype="signin", useremail=email, error=error)
				else:
					self.login(u)
					self.render("user.html", email=email)

		elif signup:
			signup_confirm_pwd = self.request.get("conf-signup-pwd")

			if pwd != signup_confirm_pwd:
				error="Password doesn't match!"
			if error:
				self.render_front(rtype="signup", useremail=email, pwd=pwd, cpwd=signup_confirm_pwd, error=error)
			else:
				# check if the email is alrady registered
				# if yes, re-render the login page with error message
				# if no, add it to database, and then redirect to user.html
				u = User.by_name(email)
				if u:
					error = "%s is already registered" % (email)
					self.render_front(rtype="signin", useremail=email, pwd=pwd, cpwd=signup_confirm_pwd, error=error) 
				else:
					u = User.register(email, pwd)
					u.put()
					self.login(u)
					self.render('/user')
		else:
			self.render_front();

class LogoutHandler(LoginHandler):
	def get(self):
		self.logout()
		self.redirect("/")	