from django.urls import path
from . import views

app_name = 'exhibitions'

urlpatterns = [
    path('', views.ExhibitionListView.as_view(), name='list'),
    path('create/', views.ExhibitionCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ExhibitionDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ExhibitionUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ExhibitionDeleteView.as_view(), name='delete'),
]
