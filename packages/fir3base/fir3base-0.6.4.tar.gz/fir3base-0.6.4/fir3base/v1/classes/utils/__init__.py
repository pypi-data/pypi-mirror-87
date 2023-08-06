#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from fir3base.v1.classes.config import * 
from django.shortcuts import render
from django.http import JsonResponse

# save & load jsons.
def __load_json__(path):
	data = None
	with open(path, "r") as json_file:
		data = json.load(json_file)
	return data
def __save_json__(path, data):
	with open(path, "w") as json_file:
		json.dump(data, json_file, indent=4, ensure_ascii=False)

# save & load files.
def __load_file__(path):
	file = open(path,mode='rb')
	data = file.read().decode()
	file.close()
	return data
def __save_file__(path, data):
	file = open(path, "w+") 
	file.write(data)
	file.close()

# save & load bytes.
def __load_bytes__(path):
	data = None
	with open(path, "rb") as file:
		data = file.read()
	return data
def __save_bytes__(path, data):
	with open(path, "wb") as file:
		file.write(data)
		
# the default response.
def __default_response__():
	return {
		"success":False,
		"error":None,
		"message":None,
	}

# get the client ip of a request.
def __get_client_ip__(request):
	try:
	    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	    if x_forwarded_for:
	        ip = x_forwarded_for.split(',')[0]
	    else:
	        ip = request.META.get('REMOTE_ADDR')
	    return ip
	except: return "unkown"

# check signed in.
# (must include the id_token url parameter.)
def __check_signed_in__(request, json=True):

	# get id token.
	parameters, response = r3sponse.get_request_parameters(request, [
		"id_token",])
	if response["error"] != None: 
		if not json:
			return response, render(request, "authentication/signin.html", {
				"COLORS":COLORS,
			})
		else: 
			return response, JsonResponse(response)

	# verify id token.
	response = firebase.users.verify_id_token(parameters["id_token"])
	if response["error"] != None:
		if not json:
			return response, render(request, "authentication/signin.html", {
				"COLORS":COLORS,
			})
		else: 
			return response, JsonResponse(response)
	else:
		return response, JsonResponse(response)

# the color object.
class Color(object):
	def __init__(self):
		self.purple = "\033[95m"
		self.cyan = "\033[96m"
		self.darkcyan = "\033[35m"
		self.orange = '\033[33m'
		self.blue = "\033[94m"
		self.green = "\033[92m"
		self.yellow = "\033[93m"
		self.grey = "\033[90m"
		self.marked = "\033[100m"
		self.markedred = "\033[101m"
		self.markedgreen = "\033[102m"
		self.markedcyan= "\033[103m"
		self.unkown = "\033[2m"
		self.red = "\033[91m"
		self.bold = "\033[1m"
		self.underlined = "\033[4m"
		self.end = "\033[0m"
		self.italic = "\033[3m"
	def remove(self, string):
		if string == None: return string
		for x in [color.purple,color.cyan,color.darkcyan,color.orange,color.blue,color.green,color.yellow,color.grey,color.marked,color.markedred,color.markedgreen,color.markedcyan,color.unkown,color.red,color.bold,color.underlined,color.end,color.italic]: string = string.replace(x,'')
		return string
	def fill(self, string):
		if string == None: return string
		for x in [
			["&PURPLE&", color.purple],
			["&CYAN&", color.cyan],
			["&DARKCYAN&", color.darkcyan],
			["&ORANGE&", color.orange],
			["&BLUE&", color.blue],
			["&GREEN&", color.green],
			["&YELLOW&", color.yellow],
			["&GREY&", color.grey],
			["&RED&", color.red],
			["&BOLD&", color.bold],
			["&UNDERLINED&", color.underlined],
			["&END&", color.end],
			["&ITALIC&", color.italic],
		]: string = string.replace(x[0],x[1])
		return string
	def boolean(self, boolean, red=True):
		if boolean: return color.green+str(boolean)+color.end
		else: 
			if red: return color.red+str(boolean)+color.end
			else: return color.yellow+str(boolean)+color.end

# the symbol object.
class Symbol(object):
	def __init__(self):
		self.cornered_arrow = color.grey+'↳'+color.end
		self.cornered_arrow_white = '↳'
		self.good = color.bold+color.green+"✔"+color.end
		self.good_white = "✔"
		self.bad = color.bold+color.red+"✖"+color.end
		self.bad_white = "✖"
		self.medium = color.bold+color.orange+"✖"+color.end
		self.pointer = color.bold+color.purple+"➤"+color.end
		self.star = color.bold+color.yellow+"★"+color.end
		self.ice = color.bold+color.cyan+"❆"+color.end
		self.retry = color.bold+color.red+"↺"+color.end
		self.arrow_left = color.end+color.bold+"⇦"+color.end
		self.arrow_right = color.end+color.bold+"⇨"+color.end
		self.arrow_up = color.end+color.bold+"⇧"+color.end
		self.arrow_down = color.end+color.bold+"⇩"+color.end
		self.copyright = color.bold+color.grey+"©"+color.end
		self.heart = color.bold+color.red+"♥"+color.end
		self.music_note = color.bold+color.purple+"♫"+color.end
		self.celcius = color.bold+color.grey+"℃"+color.end
		self.sun = color.bold+color.yellow+"☀"+color.end
		self.cloud = color.bold+color.grey+"☁"+color.end
		self.moon = color.bold+color.blue+"☾"+color.end
		self.smiley_sad = color.bold+color.red+"☹"+color.end
		self.smiley_happy = color.bold+color.green+"☺"+color.end
		self.infinite = color.bold+color.blue+"∞"+color.end
		self.pi = color.bold+color.green+"π"+color.end
		self.mode = color.bold+color.purple+"ⓜ"+color.end
		self.action = color.bold+color.yellow+"ⓐ"+color.end
		self.info = color.bold+color.grey+"ⓘ"+color.end

	#

# default initialized classes.
color = Color()
symbol = Symbol()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formatdate

# the email object class.
class Email(object):
	def __init__(self, 
		email=None, # must be first parameter.
		password=None, # must be second parameter.
		smtp_host="smtp.gmail.com", 
		smtp_port=587, 
		use_tls=True,
	):
		self.email = email
		self.password = password
		self.smtp_host = smtp_host
		self.smtp_port = smtp_port
		self.use_tls = use_tls
		self.smtp = None
	def login(self, timeout=3):
		response = __default_response__()

		# try.
		try:
			smtp = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=timeout)
			if self.use_tls:
				smtp.starttls()
			smtp.login(self.email, self.password)
			self.smtp = smtp
		except AttributeError:
			response["error"] = "Define the email address & password."
			return response
		except smtplib.SMTPAuthenticationError:
			response["error"] = "Failed to log in, provided an incorrect email and password."
			return response
		except OSError as e:
			if "Network is unreachable" in str(e):
				response["error"] = "Failed to log in, the network is unreachable. Make sure you provided the correct smtp host & port."
				return response
			else:
				response["error"] = f"Failed to log in, error: {e}."
				return response

		# response.
		response["success"] = True
		response["message"] = f"Successfully logged in to the email [{self.email}]."
		return response
	def send(self,
		# the email's subject.
		subject="Subject.",
		# define either html or html_path.
		html=None,
		html_path=None,
		# the email's recipients.
		recipients=[],
		# optional attachments.
		attachments=[],
	):

		# checks.
		response = __default_response__()
		if html != None: a=1
		elif html_path == None: 
			response["error"] = "Define either parameter [html] or [html_path]."
			return response
		else: html = utils.__load_file__(html_path)
		if len(recipients) == 0: 
			response["error"] = "Define one or multiple recipients"
			return response

		# create message.
		try:

			msg = MIMEMultipart('alternative')
			msg['From'] = self.email
			msg["To"] = ", ".join(recipients)
			msg['Date'] = formatdate(localtime=True)
			msg['Subject'] = subject
			
			# Create the body of the message (a plain-text and an HTML version).
			part1 = MIMEText("", 'plain')
			part2 = MIMEText("""\
				""" + html, 'html')
			msg.attach(part1)
			msg.attach(part2)
			for f in attachments or []:
				with open(f, "rb") as fil:
					part = MIMEApplication(
						fil.read(),
						Name=os.path.basename(f)
					)
				part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
				msg.attach(part)
			self.smtp.sendmail(self.email, recipients, msg.as_string())

			# response.
			response["success"] = True
			response["message"] = f"Succesfully send the email to {recipients}."
			return response
		except:
			response["error"] = f"Failed send the email to {recipients}."
			return response
