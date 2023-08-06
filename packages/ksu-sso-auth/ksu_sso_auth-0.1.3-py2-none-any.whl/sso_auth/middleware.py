from django.utils.deprecation import MiddlewareMixin
from .backends import TokenAuth


class OauthMiddleware(MiddlewareMixin):
	def process_request(self, request) -> None:
		if request.COOKIES.get('access_token', False):
			user = TokenAuth.authenticate(request=request)
			if user:
				request.user = request._cached_user = user
