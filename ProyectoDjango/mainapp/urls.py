from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"), #configuracion de ruta vacia vinculada al index
    path('inicio/', views.index, name="inicio"), #cuando encuentre la ruta inicio
]