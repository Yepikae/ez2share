from django.urls import path
from . import views

urlpatterns = [
    path('upload/<str:name>/', views.upload, name='upload'),
    path('ajax/upload_files/', views.upload_files, name='upload_files'),
    path('upload_complete/', views.upload_complete, name='upload_complete'),
]
