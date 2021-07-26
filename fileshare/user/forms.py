import calendar
import datetime

from django import forms
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget
from django.utils.datastructures import MultiValueDict
from guardian.shortcuts import assign_perm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Div, Field, MultiWidgetField
from crispy_forms.bootstrap import StrictButton, FormActions

from . import models
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput,
                                help_text="Enter the same password as before, for verification.")

    class Meta:
        model = models.User
        fields = ('email', 'name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password doesn't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {user} is already in use.')

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            assign_perm('fileup.add_userfile', user)
            assign_perm('user.view_user', user)
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField(
                'email',
                'name',
                'password1',
                'password2',
            ),
            FormActions(
                StrictButton('Sign up', css_class='btn btn-outline-dark btn-lg', type='submit',
                             id='signup'),
            ),
        )


class UsrChangeForm(UserChangeForm):
    date_birth = forms.DateField(widget=SelectDateWidget(years=range(1900, 2022),
                                                         empty_label=("Year", "Month", "Day")),
                                 input_formats=settings.DATE_INPUT_FORMATS,
                                 required=False)

    class Meta:
        model = models.User
        fields = ('email', 'name', 'profile_image', 'about_me', 'date_birth')

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {user} is already in use.')

    def __init__(self, data, *args, **kwargs):
        initial = kwargs.get("initial", {})
        data = MultiValueDict({**{k: [v] for k, v in initial.items()}, **data})
        super().__init__(data, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(Field(
                'profile_image', onchange="readURL(this)"), css_class='d-none'),
            FloatingField(
                Div(Div('name', css_class='col-md-4 text-center'),
                    Div('email', css_class='col-md-4 text-center'), css_class='row justify-content-md-center'),
                Div(MultiWidgetField('date_birth',
                                     attrs=({'style': 'width: 15%; display: inline-block;'}),
                                     css_class='col-md-4 text-center'), css_class='row'),
                Div(Div('about_me', style="height: auto", css_class='col text-center'), css_class='row')
            ),
            FormActions(
                StrictButton('Save changes', css_class='btn btn-outline-warning', type='submit',
                             id='edit_profile'),
                HTML("""<a href="{% url 'user:account' user_id=request.user.id %}">
                <button class="btn btn-outline-light">Back profile</button></a>"""),
            ),
        )

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.profile_image = self.cleaned_data['profile_image']
        user.about_me = self.cleaned_data['about_me']
        user.date_birth = self.cleaned_data['date_birth']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField(
                'username',
                'password',
            ),
            FormActions(
                StrictButton('Login', css_class='btn btn-outline-dark btn-lg', type='submit', id='login'),
            ),
        )


class PassChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PassChangeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField(
                'old_password',
                'new_password1',
                'new_password2',
            ),
            FormActions(
                StrictButton('Change password', css_class='btn btn-outline-warning',
                             type='submit', id='change_password'),
                HTML("""<a href="{% url 'user:account' user_id=request.user.id %}">
                        <button type="button" class="btn btn-outline-light">Back profile</button></a>"""),
            ),
        )
