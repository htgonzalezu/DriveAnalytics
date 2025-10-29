from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("vehiculos/", views.lista_vehiculos, name="lista_vehiculos"),
    path("upload/", views.upload_file, name="upload_file"),
    path("analytics/", views.analytics, name="analytics"),
]