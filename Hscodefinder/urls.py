from django.urls import path
from . import views

urlpatterns = [
    path('hscodelist/', views.hscodelist),
    
]
