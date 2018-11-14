from django.urls import path
from . import views

urlpatterns = [
    path('upload/<str:name>/', views.upload, name='upload'),
    path('ajax/upload_files/', views.upload_files, name='upload_files'),
    path('upload_complete/', views.upload_complete, name='upload_complete'),
    path('download/<str:name>/', views.download, name='download'),
    path('ajax/download_files/', views.download_files, name='download_files'),
]
