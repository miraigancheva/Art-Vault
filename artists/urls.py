from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('', views.ArtistListView.as_view(), name='list'),
    path('add/', views.ArtistCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ArtistDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ArtistUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ArtistDeleteView.as_view(), name='delete'),
]
