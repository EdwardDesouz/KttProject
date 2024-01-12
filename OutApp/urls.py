from django.urls import path
from . import views

urlpatterns = [
    path("OutList/", views.OutList),
    path("outListTable/", views.outListTable.as_view()),
    path("Out/", views.OutNew.as_view()), 
    path("OutParty/", views.OutParty.as_view()),
    path("OutParty1/", views.PartyLoad.as_view()),
    path("ParytManFacture/", views.ParytManFacture.as_view()),
    path("CargoLocations/", views.CargoLocations.as_view()),
    path("OutInvoice/<Permit>/", views.OutInvoice.as_view()),
    path("OutInvoice/", views.OutInvoice.as_view()),
    path("OutItemInhouse/", views.OutItemInhouse.as_view()),
    path("OutHscode/", views.OutHscode.as_view()),
    path("OutItem/<Permit>/", views.OutItem.as_view()),
    path("OutItem/", views.OutItem.as_view()),
    path("OutItemDelete/", views.outItemDelete),
    path("outSaveSubmit/", views.outSaveSubmit.as_view()),
    path("OutContainer/", views.ContainerSave.as_view()),
    path("AttachOut/", views.AttachDocument.as_view()),
    path("outEdit/<id>/", views.OutEdit.as_view()),
    path("CpcFIlter/<permitId>/", views.CpcFIlter.as_view()),
    path("OutItemExcelUpload/", views.ItemInNonExcelUpload.as_view()),
    path("OutPaymentCopy/<id>/", views.CopyOutPayment.as_view()),
    path("OutExcelDownload/", views.ItemExcelDownload),
    path("outEditItemall/", views.outEditItemall),
    path("outTransmit/", views.outTransmit),
    path('OutDelete/<id>/',views.OutDelete.as_view())
]
