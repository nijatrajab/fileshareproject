from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import list, detail, edit, View
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin, LoginRequiredMixin
from guardian.shortcuts import assign_perm, remove_perm
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from asgiref.sync import sync_to_async

from .models import UserFile
from .mixins import ShareMixin
from user.models import User

from .forms import FileModelForm


class FileListView(PermissionListMixin, list.ListView):
    model = UserFile

    template_name = 'fileup/ownfiles.html'
    permission_required = ['fileup.view_userfile', 'fileup.delete_userfile']
    permission_denied_message = 'You have not permission to see this'
    context_object_name = 'files'


class FileSharedListView(PermissionListMixin, ShareMixin, list.ListView):
    model = UserFile

    template_name = 'fileup/sharedfiles.html'
    permission_required = 'fileup.view_userfile'
    permission_denied_message = 'You have not permission to see this'
    context_object_name = 'files'


class FileUploadView(LoginRequiredMixin, SuccessMessageMixin, edit.CreateView):
    model = UserFile
    form_class = FileModelForm

    template_name = 'fileup/file_upload.html'
    permission_denied_message = 'You have not permission to see this'
    success_message = 'File named %(title)s has been uploaded'
    success_url = reverse_lazy('fileup:list')

    def form_valid(self, *args, **kwargs):
        file = super().form_valid(*args, **kwargs)
        assign_perm('fileup.view_userfile', self.request.user, self.object)
        assign_perm('fileup.change_userfile', self.request.user, self.object)
        assign_perm('fileup.delete_userfile', self.request.user, self.object)
        return file


class FileUpdateView(PermissionRequiredMixin, SuccessMessageMixin, edit.UpdateView):
    model = UserFile
    form_class = FileModelForm

    template_name = 'fileup/file_update.html'
    permission_required = ['fileup.view_userfile', 'fileup.change_userfile']
    permission_denied_message = 'You have not permission to see this'
    return_403 = True
    info_message = 'File was updated.'
    success_url = reverse_lazy('fileup:list')

    def form_valid(self, *args, **kwargs):
        new_file = super().form_valid(*args, **kwargs)
        messages.info(self.request, self.info_message)
        return new_file


class FileDetailView(PermissionRequiredMixin, detail.DetailView):
    model = UserFile

    template_name = 'fileup/file_detail.html'
    permission_required = 'fileup.view_userfile'
    permission_denied_message = 'You have not permission to see this'
    return_403 = True


class FileDeleteView(PermissionRequiredMixin, SuccessMessageMixin, edit.DeleteView):
    model = UserFile

    template_name = 'fileup/file_delete.html'
    permission_required = ['view_userfile', 'delete_userfile']
    permission_denied_message = 'You have not permission to see this'
    return_403 = True
    success_message = 'File was deleted.'
    success_url = reverse_lazy('fileup:list')

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return super(FileDeleteView, self).delete(request, *args, **kwargs)


class BulkDeleteView(View):
    model = UserFile

    def post(self, request, *args, **kwargs):
        selected_file = self.model.objects.filter(pk__in=request.POST['file_id'].split(','))
        if selected_file:
            delete_count = selected_file.count()
            selected_file.delete()
            if delete_count == 1:
                messages.warning(request, 'The file has been deleted.')
            else:
                messages.warning(request, '{} files have been deleted.'.format(delete_count))
        else:
            messages.error(request, 'Something bad happened!')

        return redirect('fileup:list')


class AdminPage(PermissionRequiredMixin, list.ListView):
    model = UserFile
    users = User.objects.all()
    login_url = ''

    template_name = 'fileup/admin.html'
    context_object_name = 'files'
    extra_context = {'users': users}
    raise_exception = True
    permission_required = ['is_staff', ]
    permission_denied_message = 'You have not permission to see this'
    return_403 = True
    redirect_field_name = 'next'


@login_required()
def share_file(request, id):
    usids = request.POST.getlist('user_id')
    usobjs = User.objects.filter(id__in=usids)
    obj = UserFile.objects.get(id=id)
    success_name = ', '.join(str(u.name) for u in usobjs)
    messages.success(request, f'Your have shared {obj.title} with {success_name}.')
    assign_perm('fileup.view_userfile', usobjs, obj)
    return redirect(reverse('fileup:list'))


@login_required()
def revoke_access(request, id):
    usids = request.POST.getlist('user_id')
    usobjs = User.objects.filter(id__in=usids)
    obj = UserFile.objects.get(id=id)

    users_names_list = [u.name for u in usobjs]
    users_names = ', '.join(map(str, users_names_list))

    if usobjs:
        messages.warning(request, f"You have revoked {users_names}'s permission to view {obj.title}.")
        for i in usobjs:
            remove_perm('fileup.view_userfile', i, obj)
    else:
        messages.error(request, f"You must choose user to revoke permission to view {obj.title}.")

    return redirect(reverse('fileup:list'))

