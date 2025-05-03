from django.urls import path
from .views import (AdListView, AdDetailView, AdCreateView, AdUpdateView, AdDeleteView,
                    ProposalListView, ProposalCreateView, ProposalUpdateStatusView)

app_name = "ads"

urlpatterns = [
    path('', AdListView.as_view(), name='ad_list'),
    path('me/', AdListView.as_view(me=True), name='ad_my_list'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('create/', AdCreateView.as_view(), name='create_ad'),
    path('<int:pk>/edit/', AdUpdateView.as_view(), name='update_ad'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='delete_ad'),
    path('proposals/', ProposalListView.as_view(), name='proposal_list'),
    path('proposals/create/<int:ad_receiver_id>/', ProposalCreateView.as_view(), name='proposal_create'),
    path('proposals/update/<int:pk>/', ProposalUpdateStatusView.as_view(), name='proposal_update_status'),
]
