#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fir3base.v1.classes.config import *
from fir3base.v1.classes import utils
from firebase_admin import _auth_utils
# the firebase class.
class Firebase(object):
	def __init__(self, key=None):
		
		# initialize firestore.
		# (in classes.config)
		cred = credentials.Certificate(key) # must still be edited through env variables.
		firebase_admin.initialize_app(cred)
		self.firestore = FireStore()
		self.users = Users(firestore=self.firestore)

		#

# the users class.
class Users(object):
	def __init__(self, firestore=None):

		# objects.
		self.firestore = firestore

		# settings for saving user data.
		self.users_collection = "users/"

		# the settings for sending emails.
		self.email_address = None
		self.email_password = None
		self.smtp_host = "smtp.gmail.com"
		self.smtp_port = 587

		# system variables.
		self.verification_codes = {}

		#
	def get(self, 
		# define one of the following parameters.
		uid=None,
		email=None,
		phone_number=None,
	):
		try:
			user, variable = None, None
			if uid not in [None, "None", ""]:
				user = auth.get_user(uid)
				variable = str(uid)
			elif email not in [None, "None", ""]:
				user = auth.get_user_by_email(email)
				variable = str(email)
			elif phone_number not in [None, "None", ""]:
				user = auth.get_user_by_phone_number(phone_number)
				variable = str(phone_number)
			else:
				return r3sponse.error_response("Invalid usage, define one of the following parameters: [uid, email, phone_number].")
		except _auth_utils.UserNotFoundError:
			return r3sponse.error_response("User does not exist.")

		# check success.
		if user == None: 
			return r3sponse.error_response(f"Failed to retrieve user [{variable}].")
		else:
			return r3sponse.success_response(f"Successfully retrieved user [{variable}].", {"user":user})


		#
	def create(self,
		# required:
		email=None,
		password=None,
		verify_password=None,
		# optionals:
		name=None,
		phone_number=None,
		photo_url=None,
	):

		# check parameters.
		response = r3sponse.check_parameters(empty_value=None, parameters={
			"email":email,
			"password":password,
			"verify_password":verify_password,
		})

		# check password.
		password = str(password)
		verify_password = str(verify_password)
		if len(password) < 8:
			return r3sponse.error_response("The password must contain at least 8 characters.")
		elif password.lower() == password:
			return r3sponse.error_response("The password must regular and capital letters.")
		elif password != verify_password:
			return r3sponse.error_response("Passwords do not match.")

		# create.
		try:
			user = auth.create_user(
			    email=email,
			    email_verified=False,
			    phone_number=phone_number,
			    password=password,
			    display_name=name,
			    photo_url=photo_url,
			    disabled=False)
			success = True
		except Exception as e: 
			success = False
			error = e

		# handle success.
		if success:
			return r3sponse.success_response(f"Successfully created user [{email}].", {
				"user":user,
				"uid":user.uid,
				"email":user.email,
			})
		else:
			return r3sponse.error_response(f"Failed to create user [{email}], error: {error}")

		#
	def update(self,
		# required:
		uid=None,
		# optionals:
		name=None,
		email=None,
		password=None,
		phone_number=None,
		photo_url=None,
		email_verified=None,
	):

		# load.
		response = self.get(uid=uid, email=email)
		if response["error"] != None: return response
		user = response["user"]

		# set defaults.
		if name == None: name = user.display_name
		if email == None: email = user.email
		if phone_number == None: phone_number = user.phone_number
		if photo_url == None: photo_url = user.photo_url
		if email_verified == None: email_verified = user.email_verified

		# create
		try:
			user = auth.update_user(
				uid,
				email=email,
				phone_number=phone_number,
				email_verified=email_verified,
				password=password,
				display_name=name,
				photo_url=photo_url,
				disabled=False)
			success = True
		except Exception as e: 
			success = False
			error = e

		# handle success.
		if success:
			return r3sponse.success_response(f"Successfully updated user [{uid}].")
		else:
			return r3sponse.error_response(f"Failed to update user [{uid}], error: {error}")

		#
	def delete(self, 
		# the user's uid.
		uid=None,
	):
		try:
			auth.delete(uid)
			success = True
		except Exception as e: 
			success = False
			error = e
		if success:
			return r3sponse.success_response(f"Successfully deleted user [{uid}].")
		else:
			return r3sponse.error_response(f"Failed to delete user [{uid}], error: {error}")
	def iterate(self):
		return auth.list_users().iterate_all()
	def verify_id_token(self, id_token):
		"""
			Javascript:
				firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
				  // Send token to your backend via HTTPS
				  // ...
				}).catch(function(error) {
				  // Handle error
				});
		"""
		try:
			decoded_token = auth.verify_id_token(id_token)
			uid = decoded_token['uid']
			if uid == None: success = False
			else: success = True
		except Exception as e: 
			success = False
			error = e
		if success:
			return r3sponse.success_response("You are signed in.", {"uid":uid})
		else:
			return r3sponse.error_response(f"You are not signed in, error: {error}")

		#
	def send_code(self, 
		# define uid or email to retrieve user.
		uid=None, 
		email=None, 
		# the clients ip.
		ip="unknown",
		# the mode id.
		mode="verification",
		# the mode title.
		title="Account Activation",
		# the html (str).
		html="",
		# optionally specify the code (leave None to generate).
		code=None,
	):

		# check email.
		try:
			self.email
		except AttributeError:
			response = self.__initialize_email__()
			if response["error"] != None: return response
				
		# save code.
		if code == None:
			code = Formats.Integer(0).generate(length=6)
		response = self.get(uid=uid, email=email)
		if response["error"] != None: return response
		user = response["user"]
		try: self.verification_codes[mode]
		except: self.verification_codes[mode] = {}
		self.verification_codes[mode][user.uid] = {
			"code":code,
			"stamp":Formats.Date().timestamp,
			"attempts":3,
		}
		
		# send email.
		response = self.email.send(
			subject=f'{title} - Verification Code',
			recipients=[user.email], 
			html=html)
		if response["error"] != None:
			response = self.__initialize_email__()
			if response["error"] != None: return response
			response = self.email.send(
				subject=f'{title} - Verification Code',
				recipients=[user.email], 
				html=html)
			if response["error"] != None: return response

		# success.
		return r3sponse.success_response(f"Successfully send a verification code to user [{user.display_name}].")

		#
	def verify_code(self, 
		# define uid or email to retrieve user.
		uid=None, 
		email=None, 
		# the user entered code.
		code=000000, 
		# the message mode.
		mode="verification",
	):
		# check mode.
		options = list(self.verification_codes.keys())
		if mode not in options:
			return r3sponse.error_response(f"Selected an invalid mode [{mode}], valid options: {options}.")

		# get user.
		response = self.get(uid=uid, email=email)
		if response["error"] != None: return response
		user = response["user"]

		# get success.
		fail = False
		try: self.verification_codes[mode]
		except: self.verification_codes[mode] = {}
		try: success = self.verification_codes[mode][user.uid]["attempts"] > 0 and str(self.verification_codes[mode][user.uid]["code"]) == str(code)
		except KeyError: fail = True

		# handle.
		if fail: 
			return r3sponse.error_response("Incorrect verification code.")
		elif not success: 
			self.verification_codes[mode][user.uid]["attempts"] -= 1
			return r3sponse.error_response("Incorrect verification code.")
		else:
			del self.verification_codes[mode][user.uid]
			return r3sponse.success_response("Successfull verification.")

		#
	def load_data(self,
		# the user's uid.
		uid=None,
	):
		response = self.firestore.load(f"{self.users_collection}/{uid}/")
		if response["error"] != None: return response
		return r3sponse.success_response(f"Successfully loaded the data of user [{uid}].", {
			"data":response["document"],
		})
	def save_data(self,
		# the user's uid.
		uid=None,
		# the user's data.
		data={},
	):
		response = self.firestore.save(f"{self.users_collection}/{uid}/", data)
		if response["error"] != None: return response
		return r3sponse.success_response(f"Successfully saved the data of user [{uid}].")
	# system functions.
	def __initialize_email__(self):
		# the email object.
		if self.email_address == None or self.email_password == None:
			return r3sponse.error_response("Define the firebase.users.email_address & firebase.users.email_password variables to send emails.")
		self.email = utils.Email(
			email=self.email_address,
			password=self.email_password,
			smtp_host=self.smtp_host,
			smtp_port=self.smtp_port,)
		response = self.email.login()
		if response["success"]:
			return r3sponse.success_response("Successfully initialized the mail object.")
		else: 
			self.email = None
			return response

# the firestore class.
class FireStore(object):
	def __init__(self):
		
		# initialize firestore.
		self.db = firestore.client()

		#
	# system functions.
	def list(self, reference):
		doc = self.__get_doc__(reference)
		try:
			doc = doc.get()
			success = True
		except: success = False
		if not success:
			return r3sponse.error_response(f"Failed to load document [{reference}].")
		if not isinstance(doc, list):
			return r3sponse.error_response(f"Reference [{reference}] leads to a document, not a collection.")
		return r3sponse.success_response(f"Successfully listed the content of collection [{reference}].", {"collection":doc})
	def load(self, reference):
		doc = self.__get_doc__(reference)
		try:
			doc = doc.get()
			success = True
		except: success = False
		if not success:
			return r3sponse.error_response(f"Failed to load document [{reference}].")
		if isinstance(doc, list):
			return r3sponse.error_response(f"Reference [{reference}] leads to a collection, not a document.")
		if not doc.exists:
			return r3sponse.error_response(f"Document [{reference}] does not exist.")
		else:
		    data = doc.to_dict()
		    return r3sponse.success_response(f"Successfully loaded document [{reference}].", {"document":data})
	def save(self, reference, data):
		doc = self.__get_doc__(reference)
		try:
			doc.set(data)
			success = True
		except: success = False
		if success:
			return r3sponse.success_response(f"Successfully saved document [{reference}].")
		else:
			return r3sponse.error_response(f"Failed to save document [{reference}].")
	def delete(self, reference):
		doc = self.__get_doc__(reference)
		try:
			doc.delete()
			success = True
		except: success = False
		if success:
			return r3sponse.success_response(f"Successfully deleted document [{reference}].")
		else:
			return r3sponse.error_response(f"Failed to delete document [{reference}].")
	# system functions.
	def __get_doc__(self, reference):
		reference = reference.replace("//", "/")
		if reference[len(reference)-1] == "/": reference = reference[:-1]
		doc, c = None, 0
		for r in reference.split("/"):
			if doc == None:
				doc = self.db.collection(r)
				c = 1
			else:
				if c == 1:
					doc = doc.document(r)
					c = 0
				else:
					doc = doc.collection(r)
					c = 1
		return doc

		


