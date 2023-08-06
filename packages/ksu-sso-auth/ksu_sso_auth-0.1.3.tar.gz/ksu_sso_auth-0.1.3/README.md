# Установка 
`pip install ksu-sso-auth`

# Настройка
В settings проекта добавить:
- 'sso_auth' в INSTALLED_APPS   
После этого выполнить команды
``` 
python3 manage.py makemigrations sso_auth
python3 manage.py migrate
```

Добавить в urls.py проекта в переменную urlpatterns выше всего остального следующий код:   
```
path('admin/login/', AdminLogin.as_view()),
path('admin/logout/', UserLogout.as_view()),
path('sso/', include('sso_auth.urls')),
```
До этого сделать импорт:
```
from django.urls import path, include
from sso_auth.views import AdminLogin, UserLogout
```

В settings проекта добавить:
- 'sso_auth.middleware.OauthMiddleware' в MIDDLEWARE
- код ниже. нужно заполнить реальными данными от сервера авторизации
```
# settings for sso login
AUTH_USER_MODEL = 'sso_auth.OauthUser'
AUTHENTICATION_BACKENDS = ('sso_auth.backends.TokenAuth',)
SSO_URL = 'http://127.0.0.1:8000/oauth/'
CLIENT_ID = '1bc2aea0-4dad-4f4a-9f3d-4e205b0fc10a'
CLIENT_SECRET = 'Zo8DtoPgu6m533ySFDfBImo0Lao_sh50dxE-EAHJCkwCrNvaPztIsOQaxdB0nKrX11o'
REDIRECT_URI = 'http://127.0.0.1:8001/sso/process'
```