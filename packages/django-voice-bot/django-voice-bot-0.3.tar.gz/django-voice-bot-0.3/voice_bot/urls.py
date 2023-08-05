from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    path('upload/', views.upload, name='views.upload'),
]
