from django.shortcuts import render
from django.views.generic import TemplateView
from artists.models import Artist
from artworks.models import Artwork
from exhibitions.models import Exhibition


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_artworks'] = Artwork.objects.select_related('artist', 'category').order_by('-created_at')[:6]
        context['upcoming_exhibitions'] = Exhibition.objects.filter(is_active=True).order_by('start_date')[:3]
        context['total_artists'] = Artist.objects.count()
        context['total_artworks'] = Artwork.objects.count()
        context['total_exhibitions'] = Exhibition.objects.count()
        return context


def custom_404(request, exception):
    return render(request, '404.html', status=404)
