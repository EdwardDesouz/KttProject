from django.urls import path

from . import views

urlpatterns = [
    path('Transhipment/',views.TransHome.as_view()),
    path('Transhipmentlist/',views.TranshList.as_view()),
    path('transhipmentnew/',views.TranshListnew.as_view()),
    path('transItem/',views.TranshItem.as_view()),
    path('transItem/<permit>/',views.TranshItem.as_view()),
]