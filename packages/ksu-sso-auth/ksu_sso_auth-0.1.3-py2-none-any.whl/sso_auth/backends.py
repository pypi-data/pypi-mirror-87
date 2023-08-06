from typing import Optional
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import Group
from django.db.utils import ProgrammingError
from .models import OauthUser
from sso_auth.services.get_user_info import GetUserInfo


class TokenAuth(BaseBackend):
	@staticmethod
	def authenticate(request, **kwargs):
		if request is not None:
			if request.COOKIES.get('access_token', False):
				return TokenAuth.get_user(request.COOKIES.get('access_token'))
				
		return None
	
	@staticmethod
	def get_user(access_token: str) -> Optional[OauthUser]:
		info = GetUserInfo.get_info(access_token)
		
		if info.get('user_id'):
			user = OauthUser()
			
			user.id = info.get('user_id')
			user.identifier = info.get('username')
			
			if 'is_staff' in info.get('groups'):
				user.is_staff = True
			else:
				user.is_staff = False
			
			if 'is_superuser' in info.get('groups'):
				user.is_superuser = True
			else:
				user.is_superuser = False
			
			user.is_active = info.get('is_active')
			user.is_anonymous = False
			user.email = info.get('email')
			
			groups = Group.objects.filter(name__in=info.get('groups'))
			
			try:
				user.groups.clear()
				user.user_permissions.clear()
			except ProgrammingError:
				pass
			
			try:
				for group in groups:
					permissions = group.permissions.all()
	
					for permission in permissions:
						user.user_permissions.add(permission.id)
					user.groups.add(group.id)
			except ProgrammingError:
				pass
				
			user.save()
			
			return user
		
		return None
