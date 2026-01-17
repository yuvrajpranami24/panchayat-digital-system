from django.urls import path
from .views import apply_certificate, application_status

urlpatterns = [
    path('', apply_certificate, name='apply'),
    path('status/', application_status, name='status'),
]
