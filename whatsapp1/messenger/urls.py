from django.urls import path
from .views import upload_files, generate_invalid_excel

urlpatterns = [
    path('upload/', upload_files, name='upload_files'),
    path('generate_invalid_excel/', generate_invalid_excel, name='generate_invalid_excel'),
]
