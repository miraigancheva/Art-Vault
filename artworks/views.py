from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Artwork, Category
from .forms import ArtworkForm, CategoryForm, ArtworkFilterForm


# ─── Artwork CRUD ─────────────────────────────────────────────────────────────

class ArtworkListView(ListView):
    model = Artwork
    template_name = 'artworks/artwork_list.html'
    context_object_name = 'artworks'
    paginate_by = 12

    def get_queryset(self):
        queryset = Artwork.objects.select_related('artist', 'category')
        form = ArtworkFilterForm(self.request.GET)
        if form.is_valid():
            q = form.cleaned_data.get('q')
            category = form.cleaned_data.get('category')
            on_display = form.cleaned_data.get('on_display')
            sort = form.cleaned_data.get('sort') or '-year_created'
            if q:
                queryset = queryset.filter(
                    Q(title__icontains=q) | Q(description__icontains=q)
                )
            if category:
                queryset = queryset.filter(category=category)
            if on_display == 'yes':
                queryset = queryset.filter(is_on_display=True)
            elif on_display == 'no':
                queryset = queryset.filter(is_on_display=False)
            if sort:
                queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ArtworkFilterForm(self.request.GET)
        return context


class ArtworkDetailView(DetailView):
    model = Artwork
    template_name = 'artworks/artwork_detail.html'
    context_object_name = 'artwork'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related artworks by same artist
        context['related_artworks'] = (
            Artwork.objects
            .filter(artist=self.object.artist)
            .exclude(pk=self.object.pk)
            .select_related('category')[:4]
        )
        return context


class ArtworkCreateView(CreateView):
    model = Artwork
    form_class = ArtworkForm
    template_name = 'artworks/artwork_form.html'
    success_url = reverse_lazy('artworks:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Artwork'
        context['submit_label'] = 'Save Artwork'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.title}" was added successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class ArtworkUpdateView(UpdateView):
    model = Artwork
    form_class = ArtworkForm
    template_name = 'artworks/artwork_form.html'
    success_url = reverse_lazy('artworks:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Edit: {self.object.title}'
        context['submit_label'] = 'Save Changes'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.title}" was updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class ArtworkDeleteView(DeleteView):
    model = Artwork
    template_name = 'artworks/artwork_confirm_delete.html'
    success_url = reverse_lazy('artworks:list')
    context_object_name = 'artwork'

    def form_valid(self, form):
        title = self.object.title
        result = super().form_valid(form)
        messages.success(self.request, f'"{title}" was deleted.')
        return result


# ─── Category CRUD ────────────────────────────────────────────────────────────

class CategoryListView(ListView):
    model = Category
    template_name = 'artworks/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all().prefetch_related('artworks')


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'artworks/category_form.html'
    success_url = reverse_lazy('artworks:category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add Category'
        context['submit_label'] = 'Create'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" created.')
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'artworks/category_form.html'
    success_url = reverse_lazy('artworks:category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Edit Category: {self.object.name}'
        context['submit_label'] = 'Save Changes'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" updated.')
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'artworks/category_confirm_delete.html'
    success_url = reverse_lazy('artworks:category-list')
    context_object_name = 'category'

    def form_valid(self, form):
        name = self.object.name
        result = super().form_valid(form)
        messages.success(self.request, f'Category "{name}" deleted.')
        return result
