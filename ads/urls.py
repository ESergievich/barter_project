from django.urls import path
from .views import AdListView, AdDetailView, AdCreateView, AdUpdateView, AdDeleteView

app_name = "ads"

urlpatterns = [
    path('', AdListView.as_view(), name='ad_list'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('create/', AdCreateView.as_view(), name='create_ad'),
    path('<int:pk>/edit/', AdUpdateView.as_view(), name='update_ad'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='delete_ad'),
]
