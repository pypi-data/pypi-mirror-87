"""aws_auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django_cognito.authentication import views
from django.conf.urls import url

urlpatterns = [
    # Exclude as not appropriate for this app?
    # path('admin/', admin.site.urls),
    url(r'^login', views.initiate_auth),
    # url(r'^logout', views.logout),
    url(r'^signup', views.sign_up),
    url(r'^forgot_password', views.forgot_password),
    url(r'^confirm_signup', views.confirm_sign_up),
    url(r'^confirm_login', views.respond_to_auth_challenge),
    url(r'^confirm_forgot_password', views.confirm_forgot_password),
    url(r'^generate_csrf', views.get_csrf)
]
