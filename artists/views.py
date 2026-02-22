from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Artist
from .forms import ArtistForm


class ArtistListView(ListView):
    model = Artist
    template_name = 'artists/artist_list.html'
    context_object_name = 'artists'
    paginate_by = 9

    def get_queryset(self):
        queryset = Artist.objects.all()
        search = self.request.GET.get('q', '')
        nationality = self.request.GET.get('nationality', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(biography__icontains=search)
            )
        if nationality:
            queryset = queryset.filter(nationality=nationality)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nationalities'] = Artist.Nationality.choices
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_nationality'] = self.request.GET.get('nationality', '')
        return context


class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'artists/artist_detail.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artworks'] = self.object.artworks.select_related('category').all()
        return context


class ArtistCreateView(CreateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'artists/artist_form.html'
    success_url = reverse_lazy('artists:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Artist'
        context['submit_label'] = 'Create Artist'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Artist "{form.instance.name}" was added successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class ArtistUpdateView(UpdateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'artists/artist_form.html'
    success_url = reverse_lazy('artists:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Edit Artist: {self.object.name}'
        context['submit_label'] = 'Save Changes'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Artist "{form.instance.name}" was updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class ArtistDeleteView(DeleteView):
    model = Artist
    template_name = 'artists/artist_confirm_delete.html'
    success_url = reverse_lazy('artists:list')
    context_object_name = 'artist'

    def form_valid(self, form):
        name = self.object.name
        result = super().form_valid(form)
        messages.success(self.request, f'Artist "{name}" was deleted.')
        return result
