from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.GerenciarArquivos.as_view(), name='index'),
    path('garquivos', views.ASGIGerenciadorArquivos.as_view(), name='garquivos'),
    #path('', views.index, name='index'),
]