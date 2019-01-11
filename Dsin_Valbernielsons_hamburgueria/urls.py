from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

app_name = 'core'
urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^login/$', auth_views.LoginView.as_view(), {'redirect_field_name': 'home'}, name='login'),
    url(r'^logout/$', auth_views.logout_then_login,  {"login_url": "ham:home"}, name='logout'),
    url(r'^', include('Hamburgueria.urls')),
]
