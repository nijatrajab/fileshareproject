import os
import cv2
import json
import base64

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import edit
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core import files

from .forms import UserCreationForm, LoginForm, PassChangeForm, UsrChangeForm
from .models import User

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"


class SignUp(edit.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'auth/signup.html'
    success_message = 'Now you can login ...'
    warning_message = 'You are already logged in ...'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(self.request, self.warning_message)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(SignUp, self).get(request, *args, **kwargs)

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


# overrided LoginView with message and redirect
class LgnView(LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'
    success_message = 'You are logged in ...'
    warning_message = 'You are already logged in ...'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(self.request, self.warning_message)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(LgnView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


# redirecting last point if exist
def get_redirect_if_exist(request):
    rdr = None
    if request.GET:
        if request.GET.get("next"):
            rdr = str(request.GET.get("next"))
    return rdr


# overrided PasswordChangeView for crispy form
class PassChangeView(PasswordChangeView):
    form_class = PassChangeForm
    template_name = 'password/password_change.html'


# account view with given data
def account_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")

    try:
        account = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponse("That user doesn't exist.")

    if account:
        context['id'] = account.id
        context['email'] = account.email
        context['name'] = account.name
        context['profile_image'] = account.profile_image.url
        context['date_birth'] = account.date_birth
        context['about_me'] = account.about_me

        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

        return render(request, "user/account.html", context)


def account_search_view(request, *args, **kwargs):
    context = {}

    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_res = User.objects.filter(email__icontains=search_query).filter(
                name__icontains=search_query).distinct()
            # user = request.user
            accounts = []
            for account in search_res:
                accounts.append((account, False))

            context['accounts'] = accounts

    return render(request, "user/account_search_result.html", context)


def account_edit_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    try:
        account = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponse("Something went wrong.")
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = UsrChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user:account", user_id=account.id)
        else:
            form = UsrChangeForm(request.POST, instance=request.user,
                                 initial={
                                     "id": account.pk,
                                     "email": account.email,
                                     "name": account.name,
                                     "date_birth": account.date_birth,
                                     "about_me": account.about_me,
                                     "profile_image": account.profile_image
                                 })
    else:
        form = UsrChangeForm(request.POST, instance=request.user,
                             initial={
                                 "id": account.pk,
                                 "email": account.email,
                                 "name": account.name,
                                 "date_birth": account.date_birth,
                                 "about_me": account.about_me,
                                 "profile_image": account.profile_image
                             })
        context['form'] = form
    context['PRF_IMG_UPLOAD_MAX_MEMORY_SIZE'] = settings.PRF_IMG_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "user/account_edit.html", context)


def save_temp_profile_image_from_base64String(imageString, user):
    INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(settings.TEMP + '/' + str(user.pk)):
            os.mkdir(settings.TEMP + '/' + str(user.pk))
        url = os.path.join(settings.TEMP + '/' + str(user.pk), TEMP_PROFILE_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += "=" * ((4 - len(imageString) % 4) % 4)
            return save_temp_profile_image_from_base64String(imageString, user)
    return None


def crop_image(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.POST and user.is_authenticated:
        try:
            imageString = request.POST.get("image")
            url = save_temp_profile_image_from_base64String(imageString, user)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get("cropX"))))
            cropY = int(float(str(request.POST.get("cropY"))))
            cropWidth = int(float(str(request.POST.get("cropWidth"))))
            cropHeight = int(float(str(request.POST.get("cropHeight"))))

            if cropX <= 0:
                cropX = 0
            if cropY <= 0:
                cropY = 0

            print(cropX, cropY)

            crop_img = img[cropY:cropY + cropHeight, cropX:cropX + cropWidth]
            cv2.imwrite(url, crop_img)
            print(user.profile_image.url)
            # if user.profile_image.url == f'/media/profile_images/user_{user.pk}/profile_image.png':
            #     user.profile_image.delete()
            user.profile_image.save("profile_image.png", files.File(open(url, "rb")))
            payload['result'] = "success"
            payload["cropped_profile_image"] = user.profile_image.url
            os.remove(url)
        except Exception as e:
            payload["result"] = "error"
            payload["exception"] = str(e)

    return HttpResponse(json.dumps(payload), content_type="application/json")
