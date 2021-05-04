from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import list, detail, edit, base
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin, LoginRequiredMixin
from guardian.shortcuts import assign_perm, remove_perm
from guardian.models import UserObjectPermission
from django.contrib.auth.decorators import login_required


from .models import User, UserFiles
from .forms import UserCreationForm
from fileshare.middleware import get_current_user

CurrentUser = get_current_user()


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


class AllFilesList(PermissionListMixin, list.ListView):
    model = UserFiles
    login_url = ''
    permission_required = ['users.view_userfiles', ]

    template_name = 'users/all_files_list.html'
    context_object_name = 'files'
    raise_exception = False
    permission_denied_message = 'You have not permission to see this'
    redirect_field_name = 'next'


class FileDetail(PermissionRequiredMixin, detail.DetailView):
    model = UserFiles
    users = User.objects.all()
    permission_required = ['view_userfiles', 'delete_userfiles']
    template_name = 'users/user_file_detail.html'
    context_object_name = 'files'
    extra_context = {'users': users}


class FileUploadView(PermissionRequiredMixin, edit.CreateView):
    model = UserFiles
    permission_object = None
    permission_required = ['users.add_userfiles']
    template_name = 'users/file_upload.html'
    fields = ['browse_file', 'title', 'description']
    success_url = reverse_lazy('home')

    def form_valid(self, *args, **kwargs):
        resp = super().form_valid(*args, **kwargs)
        assign_perm('view_userfiles', self.request.user, self.object)
        assign_perm('change_userfiles', self.request.user, self.object)
        assign_perm('delete_userfiles', self.request.user, self.object)
        return resp


class UserFilesDeleteView(PermissionRequiredMixin, edit.DeleteView):
    model = UserFiles
    success_url = reverse_lazy('users:all_files_list')
    permission_required = ['view_userfiles', 'delete_userfiles']
    template_name = 'users/file_delete_confirm.html'


class Access(PermissionRequiredMixin, list.ListView):
    model = UserObjectPermission
    login_url = ''
    permission_required = ['is_staff', ]

    template_name = 'users/access_user.html'
    context_object_name = 'access'
    raise_exception = False
    permission_denied_message = 'You have not permission to see this'
    redirect_field_name = 'next'


@login_required()
def myfiles(request):
    user = request.user
    files = UserFiles.objects.filter(uploaded_by=user).all()
    users = User.objects.all()
    return render(request, 'users/user_file_list.html', {'files': files, 'users': users})


@login_required()
def share_file(request, id):

    emails = request.POST.getlist('email')
    usobjs = User.objects.filter(email__in=emails)
    obj = UserFiles.objects.get(id=id)
    permtype = request.POST.get('permission')

    assign_perm(permtype, usobjs, obj)
    return redirect(reverse('users:detail', kwargs={'slug': obj.slug}))


@login_required()
def revoke_access(request, id):
    obj = UserFiles.objects.get(id=id)

    # emails = request.POST.getlist('email')
    # usobjs = User.objects.filter(email__in=emails)

    email = request.POST.get('email')
    usobj = User.objects.get(email=email)
    permtype = request.POST.get('permission')
    remove_perm(permtype, usobj, obj)
    return redirect(reverse('users:detail', kwargs={'slug': obj.slug}))
