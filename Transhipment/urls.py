from django.urls import path

from . import views

urlpatterns = [
    path("Transhipment/", views.TransHome.as_view()),
    path("Transhipmentlist/", views.TranshList.as_view()),
    path("transhipmentnew/", views.TranshListnew.as_view()),
    path("transItem/", views.TranshItem.as_view()),
    path("transItem/<permit>/", views.TranshItem.as_view()),
     path("TranDelHblHawb/<PermitId>/", views.TransDelHblHawb.as_view()),
    path("transParty1/", views.PartyLoad.as_view()),
    path("transfile/", views.AttachDocument.as_view()),
    path("transContainer/", views.ContainerSave.as_view()),
    path("transave/", views.TransSave.as_view()),
    path("transTransmit/", views.Transmit),
    path('transhipmentEdit/<id>/', views.TranshipmentEdit.as_view(), name='trans_edit'),
    path('transhipmentCopy/<id>/', views.TranshipmentCopy.as_view()),
    path("TranshipMentListDelete/<ID>/", views.TranshipListDelete.as_view()),
    path("cpcFIlter/<permitId>/", views.CpcFIlter.as_view()),
    path('transhow/<id>/', views.Transshow.as_view()),
    path("transEditItemall/", views.TransEditItemall),
    path("TransTransmitData/", views.TransMailTransmitData.as_view()),
]
