from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.views.generic import list, detail, edit, View
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin, LoginRequiredMixin
from guardian.shortcuts import assign_perm, remove_perm, get_objects_for_user, get_users_with_perms
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from asgiref.sync import sync_to_async

from .models import UserFile
from .mixins import ShareMixin
from user.models import User

from .forms import FileModelForm
from friend.models import FriendList

from permission.models import BigUserObjectPermission


def user_file(request, *args, **kwargs):
    context = {}
    user = request.user
    user_id = kwargs.get("user_id")

    if user.is_authenticated:
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

            try:
                friend_list = FriendList.objects.get(user=account)
            except FriendList.DoesNotExist:
                friend_list = FriendList(user=account)
                friend_list.save()
            friends = friend_list.friends.all()
            context['friends'] = friends

            is_self = True
            is_friend = False
            files = UserFile.objects.filter(uploaded_by=account)

            if user.is_authenticated and user != account:
                is_self = False
                if friends.filter(pk=user.id):
                    is_friend = True
                    files = get_objects_for_user(user, 'fileup.view_userfile').filter(uploaded_by=account)
                else:
                    is_friend = False
                    return redirect("user:account", user_id=account.id)

            elif not user.is_authenticated:
                is_self = False

            context['is_self'] = is_self
            context['is_friend'] = is_friend
            context['files'] = files

            return render(request, "fileup/myfile.html", context)
    else:
        return redirect("user:login")


# class FileListView(PermissionListMixin, list.ListView):
#     model = UserFile
#
#     template_name = 'fileup/ownfiles.html'
#     permission_required = ['fileup.view_userfile', 'fileup.delete_userfile']
#     permission_denied_message = 'You have not permission to see this'
#     context_object_name = 'files'


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

    def form_valid(self, *args, **kwargs):
        super().form_valid(*args, **kwargs)
        assign_perm('fileup.view_userfile', self.request.user, self.object)
        assign_perm('fileup.change_userfile', self.request.user, self.object)
        assign_perm('fileup.delete_userfile', self.request.user, self.object)
        return redirect(reverse('fileup:filelist', kwargs={'user_id': self.request.user.pk}))


class FileUpdateView(PermissionRequiredMixin, SuccessMessageMixin, edit.UpdateView):
    model = UserFile
    form_class = FileModelForm

    template_name = 'fileup/file_update.html'
    permission_required = ['fileup.view_userfile', 'fileup.change_userfile']
    permission_denied_message = 'You have not permission to see this'
    return_403 = True
    info_message = 'File was updated.'

    def form_valid(self, *args, **kwargs):
        super().form_valid(*args, **kwargs)
        messages.info(self.request, self.info_message)
        return redirect(reverse('fileup:filelist', kwargs={'user_id': self.request.user.pk}))


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

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        super(FileDeleteView, self).delete(request, *args, **kwargs)
        return redirect(reverse('fileup:filelist', kwargs={'user_id': self.request.user.pk}))


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

        return redirect(reverse('fileup:filelist', kwargs={'user_id': self.request.user.pk}))


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
    permission = 'fileup.view_userfile'

    n = BigUserObjectPermission()
    n.access_notification(other_users=usobjs, file=obj)
    assign_perm(permission, usobjs, obj)

    success_name = ', '.join(str(u.name) for u in usobjs)
    messages.success(request, f'Your have shared {obj.title} with {success_name}.')
    # assign_perm('fileup.view_userfile', usobjs, obj)
    return redirect(reverse('fileup:filelist', kwargs={'user_id': request.user.pk}))


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

    return redirect(reverse('fileup:filelist', kwargs={'user_id': request.user.pk}))
