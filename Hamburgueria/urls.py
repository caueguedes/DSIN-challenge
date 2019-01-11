from django.conf.urls import url, include
from . import views

app_name = 'ham'
urlpatterns = [
    url(r'^finaliza/', views.fechaProduto, name='finaliza'),
    url(r'^cancela/(?P<pk>\d+)$', views.cancelaPedido, name='cancela'),
    url(r'^remove/(?P<pk>\d+)$', views.removeProduto, name='remove'),
    url(r'^adiciona/(?P<pk>\d+)$', views.addProduto, name='adicionar'),
    url(r'^pedidos/', views.pedidos, name='pedidos'),
    url(r'^', views.home, name='home'),
]

