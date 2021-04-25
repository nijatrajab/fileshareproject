from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.views.generic import list, detail, edit, base
# from django.contrib.auth.mixins import (LoginRequiredMixin,
#                                         PermissionRequiredMixin)
from braces.views import SelectRelatedMixin
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin, LoginRequiredMixin
from guardian.forms import UserObjectPermissionsForm
from guardian.shortcuts import assign_perm
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group

from .models import User, UserFiles, UserManager
from .forms import UserCreationForm
from fileshare.middleware import get_current_user

CurrentUser = get_current_user()


# \\\\\\\\\\\\\\\\\\\\\\\\\\
# class UserAccessMixin(PermissionRequiredMixin):
#
#     def dispatch(self, request, *args, **kwargs):
#         if (not self.request.user.is_authenticated):
#             return redirect_to_login(self.request.get_full_path(),
#                                      self.get_login_url(),
#                                      self.redirect_field_name())
#
#         if not self.has_permission():
#             return redirect('/')
#         return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType


# content_type = ContentType.objects.get_for_model(UserFiles)
# permission = Permission.objects.create(
#     codename='can_view',
#     name='Can view files',
#     content_type=content_type,
# )

# def user_gains_perms(request, id):
#     users = get_object_or_404(User, id=id)
#     content_type = ContentType.objects.get_for_model(UserFiles)
#     permission = Permission.objects.get(
#         codename='view_userfiles',
#         content_type=content_type,
#     )
#     if request.method == "POST":
#         users.user_permissions.add(permission)
#         return redirect('users:my_files_list')
#     context = {'users': users}
#     return render(request, 'users/file_share_with.html', context)


class SignUp(edit.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class HomeView(LoginRequiredMixin, base.View):
    model = User

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return super(HomeView, self).dispatch(request, *args, **kwargs)


# class FileUploadView(LoginRequiredMixin, base.View):
#     form_class = UserFilesForm
#     success_url = reverse_lazy('home')
#     template_name = 'users/file_upload.html'
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST, request.FILES)
#         user = self.request.user
#         if form.is_valid():
#             form.save()
#
#             return redirect(self.success_url)
#         else:
#             return render(request, self.template_name, {'form': form})
class FilesList(PermissionListMixin, list.ListView):
    model = UserFiles
    login_url = ''
    permission_required = ['users.view_userfiles', ]

    template_name = 'users/all_files_list.html'
    context_object_name = 'myfiles'
    raise_exception = False
    permission_denied_message = 'You have not permission to see this'
    redirect_field_name = 'next'


class FileDetail(PermissionRequiredMixin, detail.DetailView):
    model = UserFiles
    permission_required = ['users.view_userfiles', ]


class FileUploadView(PermissionRequiredMixin, edit.CreateView):
    model = UserFiles
    permission_object = None
    permission_required = ['users.add_userfiles']
    template_name = 'users/file_upload.html'
    fields = ['browse_file', 'title']
    success_url = reverse_lazy('home')

    def form_valid(self, *args, **kwargs):
        resp = super().form_valid(*args, **kwargs)
        assign_perm('view_userfiles', self.request.user, self.object)
        assign_perm('change_userfiles', self.request.user, self.object)
        assign_perm('delete_userfiles', self.request.user, self.object)
        return resp


class MyFilesList(LoginRequiredMixin, list.ListView):
    model = UserFiles
    template_name = 'users/user_file_list.html'
    context_object_name = 'myfiles'


class UserFilesDeleteView(PermissionRequiredMixin, edit.DeleteView):
    model = UserFiles
    success_url = reverse_lazy('users:all_files_list')
    permission_required = ['view_userfiles', 'delete_userfiles']
    template_name = 'users/user_file_detail'


def FileDeleteView(request, id):
    files = get_object_or_404(UserFiles, id=id)
    if request.method == "POST":
        files.delete()
        return redirect('users:all_files_list')

    context = {'files': files}
    return render(request, 'users/file_delete_confirm.html', context)
