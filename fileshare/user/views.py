from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import edit, FormView
from django.http import JsonResponse
from django.contrib import messages

from .forms import UserCreationForm, LoginForm
from .models import User


class SignUp(edit.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'user/signup.html'
    success_message = 'Now you can login...'

    def form_valid(self, form, *args, **kwargs):
        valid = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return valid


def validate_username(request):
    """username availability"""
    email = request.GET.get('email', None)
    response = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(response)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'user/login.html'
    success_message = 'You are logged in...'

    def form_valid(self, form):
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)

        # Check here if the user is an admin
        if user is not None and user.is_active:
            login(self.request, user)
            messages.success(self.request, self.success_message)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return self.form_invalid(form)

