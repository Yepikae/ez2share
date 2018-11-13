from django.urls import path
from . import views

urlpatterns = [
    path('upload/<str:name>/', views.upload, name='upload'),
]
