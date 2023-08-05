from types import SimpleNamespace as Namespace
import requests
import json

class BosslikeExecutors:
	def __init__ (self, key):
		self.__headers = {
				'X-Api-Key': key,
				'accept': 'application/json'
			}

		self.url = 'https://api-public.bosslike.ru'

		self.urlbots = '/v1/bots/'

		self.usersme = f'{self.urlbots}users/me/'

	def __req (self, url, params = {}, methot = 'GET'):
		methot = methot.lower()
		if methot == 'get':
			req = requests.get(self.url+url, params=params, headers=self.__headers)
		elif methot == 'post':
			req = requests.post(self.url+url, data=params, headers=self.__headers)
		elif methot == 'delete':
			req = requests.delete(self.url+url, params=params, headers=self.__headers)
		
		return json.loads(req.text, object_hook=lambda d: Namespace(**d))

	def errors (self, conclusion, dop = False, i = 0):
		try:
			if not conclusion.errors:
				if dop == False:
					return conclusion
				else:
					return dop
			else:
				return conclusion.errors[i].message
		except:
			if dop == False:
				return conclusion
			else:
				return dop

	def appheaders (self, headers, look = False):
		__types = type(headers)
		if isinstance(headers, dict):
			self.__headers.update(headers)
			if look == False:
				return True
			elif look == True:
				return self.__headers
		else:
			print(f"headers must be of the dict type, and you entered: {__types}")

	def users_me (self, Error = True):
		x = self.__req(
			url=self.usersme
		)
		if Error == True:
			return self.errors(x)
		elif Error == False:
			return x

	def socials (self, Error = True):
		x = self.__req(
			url=f"{self.usersme}socials/"
		)
		if Error == True:
			return self.errors(x)
		elif Error == False:
			return x

	def delete_social (self, type, Error = True):
		x = self.__req(
			url=f"{self.usersme}social/",
			params={'type': type},
			methot='delete'
		)
		if Error == True:
			return self.errors(x)
		elif Error == False:
			return x

	def check_profile (self, url, type, token = False, Error = True):
		x = self.__req(
			url=f"{self.usersme}social/auth/like/check-profile/",
			params={'url': url,'type': type},
			methot='post'
		)
		if token == False:
			if Error == True:
				return self.errors(x)
			elif Error == False:
				return x
		elif token == True:
			try:
				if Error == True:
					return self.errors(x, x.data.token)
				elif Error == False:
					return x
			except:
				if Error == True:
					return self.errors(x)
				elif Error == False:
					return x

	def show_like (self, token, Error = True):
		x = self.__req(
			url=f"{self.usersme}social/auth/like/show-like/",
			params={'token': token},
			methot='get'
		)
		if Error == True:
			return self.errors(x)
		elif Error == False:
			return x

	def check_like (self, token, Error = True):
		x = self.__req(
			url=f"{self.usersme}social/auth/like/check-like/",
			params={'token': token},
			methot='get'
		)
		if Error == True:
			return self.errors(x)
		elif Error == False:
			return x

	def bost_tasks (self, serviceType, taskType, jsons = False, i = 0):
		x = self.__req(
			url=f"{self.urlbots}tasks/",
			params={'service_type': serviceType, 'task_type': taskType},
			methot='get'
		)
		if jsons == False:
			return x
		elif jsons == True:
			if i != True:
				return x.data.items[i].id
			elif i == True:
				arr = []
				for key in x.data.items:
					arr.append(key.id)
				return arr
		else:
			return x

	def task_do (self, id, url = False, point = False):
		x = self.__req(
			url=f"{self.urlbots}tasks/{id}/do/",
			params={'id': id},
			methot='get'
		)
		if url == False and point == False:
			return x
		elif url == True and point == False:
			return x.data.url
		elif point == True and url == False:
			return x.data.user_price
		elif url == True and point == True:
			data = '{"url": "'+x.data.url+'", "point": "'+x.data.user_price+'"}'
			x = json.loads(str(data), object_hook=lambda d: Namespace(**d))
			return x

	def task_check (self, id, Error = True):
		x = self.__req(
			url=f"{self.urlbots}tasks/{id}/check/",
			params={'id': id},
			methot='get'
		)
		if Error == True:
			return self.errors(x)
		elif Error == False:
			return x