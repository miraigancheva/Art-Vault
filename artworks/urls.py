from django.urls import path
from . import views

app_name = 'artworks'

urlpatterns = [
    # Artworks
    path('', views.ArtworkListView.as_view(), name='list'),
    path('add/', views.ArtworkCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ArtworkDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ArtworkUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ArtworkDeleteView.as_view(), name='delete'),
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
]
