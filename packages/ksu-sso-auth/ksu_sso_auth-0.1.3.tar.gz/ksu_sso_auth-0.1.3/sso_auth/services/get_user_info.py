import json
import requests
from django.conf import settings


class GetUserInfo(object):
	"""
	request to sso server to get user's info
	"""
	@staticmethod
	def get_info(access_token: str) -> dict:
		url = f'{settings.SSO_URL}info'
		
		headers = {
			'Authorization': 'Bearer {}'.format(access_token)
		}
		
		response = requests.get(url, headers=headers)
		
		if response.status_code == 200:
			info = json.loads(response.text)
			return info
		else:
			return {}
