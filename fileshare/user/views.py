from django.urls import reverse_lazy
from django.views.generic import edit

from .forms import UserCreationForm


class SignUp(edit.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'user/signup.html'