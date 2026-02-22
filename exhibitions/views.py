from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Exhibition
from .forms import ExhibitionForm


class ExhibitionListView(ListView):
    model = Exhibition
    template_name = 'exhibitions/exhibition_list.html'
    context_object_name = 'exhibitions'

    def get_queryset(self):
        status = self.request.GET.get('status', 'active')
        if status == 'all':
            return Exhibition.objects.prefetch_related('artworks').all()
        return Exhibition.objects.filter(is_active=True).prefetch_related('artworks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', 'active')
        return context


class ExhibitionDetailView(DetailView):
    model = Exhibition
    template_name = 'exhibitions/exhibition_detail.html'
    context_object_name = 'exhibition'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artworks'] = self.object.artworks.select_related('artist', 'category').all()
        return context


class ExhibitionCreateView(CreateView):
    model = Exhibition
    form_class = ExhibitionForm
    template_name = 'exhibitions/exhibition_form.html'
    success_url = reverse_lazy('exhibitions:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Exhibition'
        context['submit_label'] = 'Create Exhibition'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Exhibition "{form.instance.title}" created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class ExhibitionUpdateView(UpdateView):
    model = Exhibition
    form_class = ExhibitionForm
    template_name = 'exhibitions/exhibition_form.html'
    success_url = reverse_lazy('exhibitions:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Edit Exhibition: {self.object.title}'
        context['submit_label'] = 'Save Changes'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Exhibition "{form.instance.title}" updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class ExhibitionDeleteView(DeleteView):
    model = Exhibition
    template_name = 'exhibitions/exhibition_confirm_delete.html'
    success_url = reverse_lazy('exhibitions:list')
    context_object_name = 'exhibition'

    def form_valid(self, form):
        title = self.object.title
        result = super().form_valid(form)
        messages.success(self.request, f'Exhibition "{title}" was deleted.')
        return result
