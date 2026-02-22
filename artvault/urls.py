from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('artists/', include('artists.urls', namespace='artists')),
    path('artworks/', include('artworks.urls', namespace='artworks')),
    path('exhibitions/', include('exhibitions.urls', namespace='exhibitions')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'artvault.views.custom_404'
