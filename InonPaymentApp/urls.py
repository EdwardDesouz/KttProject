from django.urls import path

from . import views


from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('InonPaymentList/', views.InonoList),
    path('InNonList/', views.InNonList.as_view()),
    path('InonPayement/', views.InonPayment.as_view()),
    path('InonPayementEdit/', views.InonPaymentEdit.as_view()),
    path("InonImporterSearch/", views.ImporterInon), 
    path("InNonExcelDownload/", views.InNonExcelDownload),
    path("InNonPartyLoad/", views.PartyLoad.as_view()),
    path("InNonCargoPage/", views.InNonCargoLoad.as_view()),
    path("InNonInvoiceLoad/", views.InNonInvoiceLoad.as_view()),
    path("InNonItemLoad/", views.InNonItemLoad.as_view()),
    path("ItemInNonExcelUpload/", views.ItemInNonExcelUpload.as_view()),
    path("AllItemUpdateInNon/", views.AllItemUpdateInNon.as_view()),
    path("ConsolidateInNon/", views.ConsolidateInNon.as_view()),
    path("ContainerInNon/", views.ContainerLoad.as_view()),
    path("AttachInNon/", views.AttachDocument.as_view()),
    path("InNonSave/", views.InNonSave.as_view()),
    path("InNonHeaderDelete/", views.InNonHeaderDelete.as_view()),
    path("CopyInNonPayment/", views.CopyInNonPayment.as_view()),
    path("InNonTransmitData/", views.InNonTransmitData.as_view()),
    path("XmlGenInNon/", views.XmlGen.as_view()),
    path("AttachDownloadInNon/<ID>/", views.AttachDownloadInNon),
    path("CpcDeleteInNon/<ID>/", views.CpcDeleteInNon),
    path("InonPayementAmend/<Id>/", views.InonPayementAmend.as_view()),
    path("InonPayementCancel/<Id>/", views.InonPayementCancel.as_view()),
    path("DeleteAllInNon/<Id>/", views.DeleteAllInNon.as_view()),
    path("InNonPaymentCcp/<Data>/", views.InNonPaymentCcp.as_view()),
    path("PrintGstInNon/<ID>/", views.PrintGstInNon.as_view()),
    path("PrintStatusInNon/<ID>/", views.PrintSatusInNon.as_view()),
    path("DownloadCcpInNon/<Data>/", views.DownloadCcpInNon.as_view()),
    path("InNonDelHblHawb/<PermitId>/", views.InNonDelHblHawb.as_view()),
    path("DownloadDataInNon/<Id>/", views.DownloadDataInNon.as_view()),
    path("InonSubmit/", views.InNonSubmit),  
]

router = DefaultRouter()
router.register("api/categories", views.InNonViewSet, basename="InNonPayment")


urlpatterns += router.urls
