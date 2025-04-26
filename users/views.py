from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterUserForm


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')
