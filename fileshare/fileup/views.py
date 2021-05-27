from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import list, detail, edit
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin
from guardian.shortcuts import assign_perm, remove_perm
from django.contrib.auth.decorators import login_required

from .models import UserFile
from user.models import User


class MyFilesList(PermissionListMixin, list.ListView):
    model = UserFile
    users = User.objects.all()
    login_url = ''
    permission_required = ['fileup.view_userfile', 'fileup.delete_userfile']

    template_name = 'fileup/user_file_list.html'
    context_object_name = 'files'
    extra_context = {'users': users}
    raise_exception = False
    permission_denied_message = 'You have not permission to see this'
    redirect_field_name = 'next'


class SharedWithMe(PermissionListMixin, list.ListView):
    model = UserFile
    login_url = ''
    permission_required = ['fileup.view_userfile', ]

    template_name = 'fileup/shared_with_me.html'
    context_object_name = 'files'
    raise_exception = False
    permission_denied_message = 'You have not permission to see this'
    redirect_field_name = 'next'


class FileDetail(PermissionRequiredMixin, detail.DetailView):
    model = UserFile
    users = User.objects.all()
    permission_required = ['view_userfile', 'delete_userfile']
    template_name = 'fileup/user_file_detail.html'
    context_object_name = 'files'
    extra_context = {'users': users}


class FileUploadView(PermissionRequiredMixin, edit.CreateView):
    model = UserFile
    permission_object = None
    permission_required = ['fileup.add_userfile']
    template_name = 'fileup/file_upload.html'
    fields = ['browse_file', 'title', 'description']
    success_url = reverse_lazy('home')

    def form_valid(self, *args, **kwargs):
        resp = super().form_valid(*args, **kwargs)
        assign_perm('view_userfile', self.request.user, self.object)
        assign_perm('change_userfile', self.request.user, self.object)
        assign_perm('delete_userfile', self.request.user, self.object)
        return resp


class FileDeleteView(PermissionRequiredMixin, edit.DeleteView):
    model = UserFile
    success_url = reverse_lazy('fileup:shared_with_me')
    permission_required = ['view_userfile', 'delete_userfile']
    template_name = 'fileup/file_delete_confirm.html'


class AdminPage(PermissionListMixin, list.ListView):
    model = UserFile
    users = User.objects.all()
    login_url = ''
    permission_required = ['is_staff', ]

    template_name = 'fileup/admin_page.html'
    context_object_name = 'files'
    extra_context = {'users': users}
    raise_exception = False
    permission_denied_message = 'You have not permission to see this'
    redirect_field_name = 'next'


@login_required()
def share_file(request, id):
    emails = request.POST.getlist('email')
    usobjs = User.objects.filter(email__in=emails)
    obj = UserFile.objects.get(id=id)
    permtype = request.POST.get('permission')

    assign_perm(permtype, usobjs, obj)
    return redirect(reverse('fileup:my_files_list'))


@login_required()
def revoke_access(request, id):
    obj = UserFile.objects.get(id=id)

    # emails = request.POST.getlist('email')
    # usobjs = User.objects.filter(email__in=emails)

    email = request.POST.get('email')
    usobj = User.objects.get(email=email)
    permtype = request.POST.get('permission')
    remove_perm(permtype, usobj, obj)
    return redirect(reverse('fileup:detail', kwargs={'pk': obj.pk}))
