from django.urls import path
from .views import ProcessRedirectUri


urlpatterns = [
	path('process', ProcessRedirectUri.as_view())
]
