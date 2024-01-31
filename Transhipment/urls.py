from django.urls import path

from . import views

urlpatterns = [
    path("Transhipment/", views.TransHome.as_view()),
    path("Transhipmentlist/", views.TranshList.as_view()),
    path("transhipmentnew/", views.TranshListnew.as_view()),
    path("transItem/", views.TranshItem.as_view()),
    path("transItem/<permit>/", views.TranshItem.as_view()),
    path("transParty1/", views.PartyLoad.as_view()),
    path("transfile/", views.AttachDocument.as_view()),
    path("transContainer/", views.ContainerSave.as_view()),
    path("transave/", views.TransSave.as_view()),
    path("transTransmit/", views.Transmit),
]
