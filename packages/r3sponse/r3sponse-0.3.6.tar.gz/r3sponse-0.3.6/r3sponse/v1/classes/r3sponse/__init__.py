#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from r3sponse.v1.classes.config import *
from r3sponse.v1.classes import utils
from r3sponse.v1.classes.utils import color, symbol
from django.http import JsonResponse

# the manager class.
class R3sponse(object):
	def __init__(self):	

		# set log file.
		self.log_file = None

		# set log level.
		self.log_level = 0
		if utils.argument_present('--log-level'):
			try: self.log_level = int(utils.get_argument('--log-level'))
			except: self.log_level = 0
		#

	# response functions.
	def default_response(self):
		return {
			"success":False,
			"error":None,
			"message":None,
		}
	def success_response(self,
		# the message (must be param #1).
		message, 
		# additional returnable functions (must be param #2).
		variables={}, 
		# log log level of the message (int).
		log_level=None, 
		# save the error to the logs file.
		save=False,
		# return as a django JsonResponse.
		django=False,
	):
		response = self.default_response()
		response["success"] = True
		response["message"] = message
		for key, value in variables.items():
			response[key] = value
		if log_level != None and self.log_level >= log_level: print(response["message"])
		if save: self.__log_to_file__(response["message"])
		if django: response = JsonResponse(response)
		return response
	def error_response(self,
		# the error message.
		error="", 
		# log log level of the message (int).
		log_level=None, 
		# save the error to the erros file.
		save=False,
		# return as a django JsonResponse.
		django=False,
	):
		response = self.default_response()
		response["error"] = error
		if log_level != None and self.log_level >= log_level: print(response["error"])
		if save: self.__log_to_file__(response["error"])
		if django: response = JsonResponse(response)
		return response
		#
	def success(self, response):
		if response["error"] == None:
			return True
		else: return False

	# parameter functions.
	def get_request_parameter(self, request, identifier):
		response = self.default_response()
		variable = request.GET.get(identifier)
		if variable in ["", None]:
			return variable, self.error_response(f"Define parameter: [{identifier}].")
		return variable, self.success_response(f"Succesfully retrieved request parameter [{identifier}].")
	def get_request_parameters(self, request, identifiers=[], optional=False):
		if isinstance(identifiers, str):
			return self.error_response("__get_request_params__ is used to retrieve several identifiers (array format not string).")
		params = {}
		for param in identifiers:
			param_value, response = self.get_request_parameter(request, param)
			if response["error"] != None: 
				if optional:
					params[param] = None
				else:
					return params, response
			else: 
				params[param] = param_value
		return params, response

	# check parameters.
	def check_parameter(self, parameter=None, name="parameter", empty_value=None):
		response = self.default_response()
		if parameter == empty_value: 
			return self.error_response(f"Define parameter [{name}].")
		else: return self.success_response(f"Succesfully checked parameter [{name}].")
	def check_parameters(self, parameters={"parameter":None}, empty_value=None):
		response = self.default_response()
		for id, value in parameters.items():
			response = self.check_parameter(value, id, empty_value=empty_value)
			if response["error"] != None: return response
		return response

	# log functions.
	def log(self, 
		# option 1:
		# the message.
		message=None,
		# option 2:
		# the response dict (leave message None to use).
		response={},
		# optionals:
		# the log level for printing to console.
		log_level=0,
		# save to log file.
		save=False,
		# save errors only (for option 2 only).
		save_errors=False,
	):
		msg, _error_ = None, False
		if [message,response] == [None,{}]:
			raise ValueError("Define either parameter [message:str] or [response:dict].")
		if response != {}:
			if response["error"] != None: 
				_error_ = True
				msg = f"Error: {response['error']}"
			else: 
				msg = response["message"]
		else: 
			msg = message
		if log_level >= self.log_level:
			print(color.fill(msg))
		if save: 
			self.__log_to_file__(msg)
		elif save_errors and _error_:
			self.__log_to_file__(msg)

		#
	def load_logs(self, format="webserver", options=["webserver", "cli", "array", "string"]):
		try:
			logs = Formats.File(self.log_file, load=True, blank="").data
		except:
			return self.error_response("Failed to load the logs.")
		if format == "webserver":
			logs = logs.replace("\n", "<br>")
		elif format == "cli":
			a=1
		elif format == "array" or format == list:
			logs = logs.split("\n")
		elif format == "string" or format == str:
			logs = str(logs)
		else: 
			return self.error_response(f"Invalid format parameter [{format}], valid options: {options}.")

		return self.success_response("Succesfully loaded the logs.", {"logs":logs})
	def reset_logs(self):
		Formats.File(self.log_file).save(f"Resetted log file.\n")
		#
	
	# system functions.
	def __log_to_file__(self, message):

		# init.
		response = self.default_response()
		try:
			with open(self.log_file, "a") as file:
				file.write(f'{Formats.Date().seconds_timestamp} - {message}\n')
			response["success"] = True
			response["message"] = "Succesfully logged the message."
		except:
			response["error"] = "Failed to log the message."
			return response
		
		# check file size.
		size = Formats.FilePath(self.log_file).size(mode="mb", type="integer")
		if size >= 100: self.reset_logs()

		# return response.
		return response

		#

# initialized objects.
r3sponse = R3sponse()

