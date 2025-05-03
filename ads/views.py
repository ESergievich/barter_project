from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Ad
from .utils import CategoryChoices, ConditionChoices


class AdListView(ListView):
    me = False
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-created_at']
    paginate_by = 15
    extra_context = {
        'categories': CategoryChoices,
        'conditions': ConditionChoices,
    }

    def get_queryset(self):
        if self.me:
            queryset = super().get_queryset().filter(user=self.request.user)
        else:
            queryset = super().get_queryset()
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')

        if query:
            search_query = SearchQuery(query)
            rank = SearchRank(F("search_vector"), search_query)
            queryset = queryset.annotate(rank=rank).filter(search_vector=search_query).order_by('-rank')
        if category:
            queryset = queryset.filter(category=category)
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['category'] = self.request.GET.get('category', '')
        context['condition'] = self.request.GET.get('condition', '')
        context['me'] = self.me

        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    fields = ['title', 'description', 'image_url', 'category', 'condition']
    template_name = 'ads/create_ad.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    fields = ['title', 'description', 'image_url', 'category', 'condition']
    template_name = 'ads/update_ad.html'

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/delete_ad.html'
    success_url = reverse_lazy('ads:ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user
