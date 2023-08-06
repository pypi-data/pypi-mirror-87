import json
from django.views.generic import View
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
import requests
from sso_auth.services.get_user_info import GetUserInfo
from sso_auth.services.get_token_by_refresh import GetTokenByRefresh


url = f'{settings.SSO_URL}authorize?response_type=code&client_id={settings.CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}'


# Create your views here.
class AdminLogin(View):
	"""
	redefine auth form for admin panel
	"""
	def get(self, request):
		if not request.COOKIES.get('access_token', False) or not request.COOKIES.get('refresh_token', False):
			return redirect(url)
		else:
			response = HttpResponseRedirect('/admin')
			
			info = GetUserInfo.get_info(request.COOKIES.get('access_token'))

			if not info.get('user_id'):
				# try get new access token by refresh token
				tokens = GetTokenByRefresh.get_token(request.COOKIES.get('refresh_token'))
				
				if tokens.get('access_token'):
					print(tokens.get('access_token'))
					info = GetUserInfo.get_info(tokens.get('access_token'))
					
				if not info.get('user_id') or not info.get('is_active'):
					response.delete_cookie('access_token')
					response.delete_cookie('refresh_token')
				else:
					response.set_cookie('access_token', tokens.get('access_token'))
					response.set_cookie('refresh_token', tokens.get('refresh_token'))
				
			return response
	
			
class UserLogout(View):
	"""
	user's logout
	"""
	def get(self, request):
		response = HttpResponseRedirect('https://sso.kursksu.ru/admin/logout/')
		response.delete_cookie('access_token')
		response.delete_cookie('refresh_token')
		
		return response
	
		
class ProcessRedirectUri(View):
	"""
	process grant code to receive access token
	"""
	def get(self, request):
		if not request.GET.get('code'):
			return redirect(url)
		
		data = {
			'grant_type': 'authorization_code',
			'client_id': settings.CLIENT_ID,
			'client_secret': settings.CLIENT_SECRET,
			'redirect_uri': settings.REDIRECT_URI,
			'code': request.GET.get('code')
		}
		
		response = requests.post(f'{settings.SSO_URL}token', data=data)
		
		if response.status_code == 200:
			token = json.loads(response.text)
			
			if request.session.get('custom_redirect_uri'):
				context = {
					'redirect_uri': request.session.get('custom_redirect_uri'),
				}
				
				del request.session['custom_redirect_uri']
				request.session.modified = True
			else:
				context = {
					'redirect_uri': '/admin',
				}
			content = render_to_string('success_auth.html', context)
			
			response = HttpResponse(content)
			response.set_cookie('access_token', token.get('access_token'))
			response.set_cookie('refresh_token', token.get('refresh_token'))
			
			return response
