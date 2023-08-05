import requests
import json
import time
import hashlib
import hmac
import random
import base64

_BASE_URL = 'https://wqvsv5x50d.execute-api.eu-north-1.amazonaws.com/dev'

class Client:

	def __init__(self, username, password, secret):
		'''
			Create a client object that represents your HTClient account

		'''
		self.username = username
		self.password = password
		self.secret = secret

	def _headers(self, resource, body):
		timestamp = str(int(time.time()*1000))
		msg = resource+json.dumps(body)+timestamp
		secret = self.secret
		signature = hmac.new(secret.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).hexdigest()
		return {
			'timestamp': timestamp,
			'signature': signature
		}

	def _request(self, resource, body):
		print(json.dumps(body))
		print(self._headers(resource, body))
		raw = requests.post(url=_BASE_URL+resource, data=json.dumps(body), headers=self._headers(resource, body)).text
		try:
			return json.loads(raw)
		except:
			raise Exception(raw)

	def exchange_list(self):
		'''
			Get a list of exchanges that are supported and their auth key names

		'''
		resource = '/exchangelist'
		body = {
			'username': self.username,
			'password': self.password
		}
		return self._request(resource, body)

	def account_list(self):
		'''
			Get a list of accounts

		'''
		resource = '/accountlistwithexchange'
		body = {
			'username': self.username,
			'password': self.password
		}
		return self._request(resource, body)

	def script_list(self):
		'''
			Get a list of scripts

		'''
		resource = '/scriptlistwithbrief'
		body = {
			'username': self.username,
			'password': self.password
		}
		return self._request(resource, body)

	def account_detail(self, accountName):
		'''
			Get account details of a single account

			Argument(s):
				accountName: the account name

		'''
		resource = '/accountdetail'
		body = {
			'username': self.username,
			'password': self.password,
			'accountName': accountName
		}
		resp = self._request(resource, body)
		return resp

	def change_account_auth(self, accountName, **kwargs):
		'''
			Change the authentication keys of the account

			Argument(s):
				accountName: the account name

			Keyword Argument(s):
				**auth key name: auth key value

		'''
		resource = '/changeaccountauth'
		body = {
			'username': self.username,
			'password': self.password,
			'accountName': accountName,
			'auth': kwargs
		}
		return self._request(resource, body)

	def add_account(self, name, exchange, **kwargs):
		'''
			Add a new account

			Argument(s):
				name: account name
				exchange: the account exchange

			Keyword Argument(s):
				**auth key name: auth key value

		'''
		resource = '/addaccount'
		body = {
			'username': self.username,
			'password': self.password,
			'name': name,
			'exchange': exchange,
			'auth': kwargs
		}
		return self._request(resource, body)

	def script_detail(self, scriptName):
		'''
			Get details of a single script

			Argument(s):
				scriptName: the script name

		'''
		resource = '/scriptdetail'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName
		}
		resp = self._request(resource, body)
		return resp

	def change_script_class(self, scriptName, scriptClass):
		'''
			Change the script class

			Argument(s):
				scriptName: the script name
				scriptClass: the new script class

		'''
		resource = '/changescriptclass'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName,
			'class': scriptClass
		}
		return self._request(resource, body)

	def online(self, scriptName):
		'''
			Put a script online

			Argument(s):
				scriptName: the script name

		'''
		resource = '/online'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName
		}
		return self._request(resource, body)

	def offline(self, scriptName):
		'''
			Put a script offline

			Argument(s):
				scriptName: the script name

		'''
		resource = '/offline'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName
		}
		return self._request(resource, body)

	def clear_orders(self, scriptName):
		'''
			Clear the orders of a script

			Argument(s):
				scriptName: the script name

		'''
		resource = '/clearorders'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName
		}
		return self._request(resource, body)

	def clear_storage(self, scriptName):
		'''
			Clear the storage of a script

			Argument(s):
				scriptName: the script name

		'''
		resource = '/clearstorage'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName
		}
		return self._request(resource, body)

	def attach_account(self, scriptName, accountName, accountType):
		'''
			Attach an account to the script

			Argument(s):
				scriptName: the script name
				accountName: the name of the account to be attached
				accountType: the type of the account to be attached as, e.g. main/secondary

		'''
		resource = '/attachaccount'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName,
			'accountName': accountName,
			'accountType': accountType
		}
		return self._request(resource, body)

	def change_parameters(self, scriptName, **kwargs):
		'''
			Change the config parameters of a script

			Argument(s):
				scriptName: the script name

			Keyword Argument(s):
				**parameter name: parameter value

		'''
		resource = '/changeparameters'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName,
			'config': kwargs
		}
		return self._request(resource, body)

	def add_script(self, name, scriptClass, mainAccount, secondaryAccount=None, **kwargs):
		'''
			Add a script

			Argument(s):
				name: the script name
				scriptClass: the script class
				mainAccount: main account name

			Keyword Argument(s):
				secondaryAccount: the secondary account name, default None
				**config parameters name: config parameters value

		'''
		resource = '/addscript'
		body = {
			'username': self.username,
			'password': self.password,
			'name': name,
			'scriptClass': scriptClass,
			'mainAccount': mainAccount,
			'config': kwargs,
			'status': offline
		}
		if secondaryAccount is not None:
			body['secondaryAccount'] = secondaryAccount
		return self._request(resource, body)

	def delete_account(self, accountName):
		'''
			Delete an account

			Argument(s):
				accountName: the account name

		'''
		resource = '/deleteaccount'
		body = {
			'username': self.username,
			'password': self.password,
			'accountName': accountName
		}
		return self._request(resource, body)

	def delete_script(self, scriptName):
		'''
			Delete a script

			Argument(s):
				scriptName: the script name

		'''
		resource = '/deletescript'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName
		}
		return self._request(resource, body)

	def show_balance(self, *args):
		'''
			Show the balance of an account

			Positional Argument(s):
				0: the account name
				:: currency symbols in lower case

		'''
		resource = '/showbalance'
		accountName = args[0]
		currencies = list(args[1::])
		body = {
			'username': self.username,
			'password': self.password,
			'accountName': accountName,
			'currencies': currencies
		}
		resp = self._request(resource, body)
		return resp

	def monitor(self, scriptName):
		'''
			Get the monitor of a script

			Argument(s):
				scriptName: the script name

		'''
		resource = '/monitor'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName
		}
		return self._request(resource, body)

	def get_logs(self, *args, limit=2):
		'''
			Get the server logs of a script

			Positional Argument(s):
				:: script names

			Keyword Arguments(s):
				limit: Number of logs to be returned for each script

		'''
		resource = '/getlogs'
		body = {
			'username': self.username,
			'password': self.password,
			'scripts': args,
			'limit': limit
		}
		resp = self._request(resource, body)
		return resp

	def add_custom(self, name, code, monitor, meta):
		'''
			Add a customized script class

			Argument(s):
				name: class name
				code: the code of the class as a string
				monitor: the monitor objects of the class as a json string
				meta: the script meta as a json string

		'''
		resource = '/addcustom'
		body = {
			'username': self.username,
			'password': self.password,
			'name': name,
			'code': code,
			'monitor': monitor,
			'meta': meta
		}
		return self._request(resource, body)

	def custom_class_list(self):
		'''
			Get a list of customized script classes

		'''
		resource = '/customclasslist'
		body = {
			'username': self.username,
			'password': self.password
		}
		return self._request(resource, body)

	def custom_class_detail(self, className):
		'''
			Get the details of a single customized script class

		'''
		resource = '/customclassdetail'
		body = {
			'username': self.username,
			'password': self.password,
			'className': className
		}
		resp = self._request(resource, body)
		return resp

	def update_custom_class(self, className, changes):
		'''
			Update a customized script class

			Argument(s):
				className: the class name
				changes: the details of the update as a dictionary
					keys:
						name: class name
						code: the code of the class as a string
						monitor: the monitor objects of the class as a json string
						meta: the script meta as a json string

		'''
		resource = '/updatecustomclass'
		body = {
			'username': self.username,
			'password': self.password,
			'name': className,
			'changes': changes
		}
		return self._request(resource, body)

	def delete_class(self, className):
		'''
			Delete a customized script class

			Argument(s):
				className: the class name

		'''
		resource = '/deleteclass'
		body = {
			'username': self.username,
			'password': self.password,
			'name': className
		}
		return self._request(resource, body)

	def check_inventory(self, scriptName):
		'''
			Check the recommended funding for a script

			Argument(s):
				scriptName: the script name

		'''
		resource = '/checkinventory'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName
		}
		return self._request(resource, body)

	def generate_report(self, scriptName, startTime, endTime=None):
		'''
			Get the HTML body of a script report

			Argument(s):
				scriptName: the script name
				startTime: the start time of the report in seconds

		'''
		resource = '/generatereport'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName,
			'startTime': startTime,
			'endTime': endTime
		}
		return self._request(resource, body)

	def get_script_record(self, scriptName):
		'''
			Get the script record for a script
			It includes snapshots and trade history

			Argument(s):
				scriptName: the script name

		'''
		resource = '/getscriptrecord'
		body = {
			'username': self.username,
			'password': self.password,
			'scriptName': scriptName,
		}
		return self._request(resource, body)

