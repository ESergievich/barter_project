from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .forms import ProposalForm
from .models import Ad, ExchangeProposal
from .utils import CategoryChoices, ConditionChoices, ProposalStatusChoices


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


class ProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = 'proposals/proposal_list.html'
    context_object_name = 'proposals'

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(Q(ad_sender__user=user) | Q(ad_receiver__user=user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['sent'] = ExchangeProposal.objects.filter(ad_sender__user=user)
        context['received'] = ExchangeProposal.objects.filter(ad_receiver__user=user)
        return context


class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ProposalForm
    template_name = 'proposals/proposal_form.html'

    def form_valid(self, form):
        ad_receiver = get_object_or_404(Ad, id=self.kwargs['ad_receiver_id'])

        if ad_receiver.user == self.request.user:
            return HttpResponseForbidden("Нельзя предлагать обмен себе")

        form.instance.ad_receiver = ad_receiver
        form.instance.ad_sender = form.cleaned_data['ad_sender']
        form.instance.status = ProposalStatusChoices.PENDING
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('ads:proposal_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_receiver_title'] = Ad.objects.get(id=self.kwargs['ad_receiver_id']).title
        return context


class ProposalUpdateStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        proposal = get_object_or_404(ExchangeProposal, pk=pk)

        if request.user not in [proposal.ad_receiver.user, proposal.ad_sender.user]:
            return HttpResponseForbidden("Вы не можете изменять статус этого предложения")
        if proposal.status != ProposalStatusChoices.PENDING:
            return HttpResponseForbidden("Статус уже изменен")

        status = request.POST.get('status')
        if status in ['accepted', 'rejected']:
            proposal.status = status
            proposal.save()
        return redirect('ads:proposal_list')
