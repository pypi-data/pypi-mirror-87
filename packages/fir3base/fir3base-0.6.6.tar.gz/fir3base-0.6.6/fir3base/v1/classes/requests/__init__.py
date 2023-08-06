#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fir3base.v1.classes.config import *
from fir3base.v1.classes.firebase import *
from django.http import JsonResponse

# universal variables.
firebase = None

# the users requests.
class users():

	# the sign up request.
	class signup():
		def view(request):

			# get parameters.
			parameters, response = r3sponse.get_request_parameters(request, [
				"email",
				"password",
				"verify_password",])
			if response["error"] != None: return response
			optional_parameters, _ = r3sponse.get_request_parameters(request, [
				"name",], optional=True)

			# check firebase set.
			if firebase == None:
 				return r3sponse.error_response("Set the firebase of the requests.users class. [fir3base.requests.users.firebase = your_firebase_object")

			# make request.
			response = firebase.users.create(
				name=optional_parameters["name"],
				email=parameters["email"],
				password=parameters["password"],
				verify_password=parameters["verify_password"],
			)
			try:
				if response["success"]: del response["user"]
			except KeyError: a=1
			return response

	# verify code.
	class verify_code():
		def view(request):
			
			# get parameters.
			parameters, response = r3sponse.get_request_parameters(request, [
				"code",
				"mode",
				"uid",])
			if response["error"] != None: return JsonResponse(response)

			# make request.
			response = firebase.users.verify_code(
				code=parameters["code"], 
				uid=parameters["uid"], 
				mode=parameters["mode"])
			if response["error"] != None: return JsonResponse(response)

			# save email verified.
			response = firebase.users.update(
				uid=parameters["uid"],
				email_verified=True,)
			if response["error"] != None: return JsonResponse(response)
			else: return r3sponse.success_response("Successfully activated your account.", django=True)


	# send code.
	class send_code():
		def view(request):
			
			# get parameters.
			parameters, response = r3sponse.get_request_parameters(request, [
				"mode",
				"uid",])
			if response["error"] != None: return JsonResponse(response)

			# make request.
			return JsonResponse(firebase.users.send_code(
				uid=parameters["uid"], 
				mode=parameters["mode"],
				title="Account Activation",
				html=None, ))
