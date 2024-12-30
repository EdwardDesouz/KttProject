from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('hscodelist/', views.hscodelist),
    path('partypage', PartyPage.as_view(), name='party_page'),
    path('inwardget', InwardGet.as_view(), name='inward_get'),
    path('importerget', ImporterGet.as_view(), name='importer_get'),
    path('importerupdate',ImporterUpdate.as_view(),name='importer_update'),
    path('freightforwarderget',FreightForwarderGet.as_view(),name='frightforwarder_get'),
    path('freightforwarderupdate',FreightForwarderUpdate.as_view(),name='freightforwarder_update'),



    
    
]
