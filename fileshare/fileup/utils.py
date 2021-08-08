from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Q
from guardian.ctypes import get_content_type
from guardian.shortcuts import get_perms, get_user_perms
from guardian.utils import get_user_obj_perms_model, get_group_obj_perms_model


def get_users_timestamp_with_perms(obj, attach_perms=False, with_superusers=False,
                                   with_group_users=True, only_with_perms_in=None):
    ctype = get_content_type(obj)
    if not attach_perms:
        # It's much easier without attached perms so we do it first if that is
        # the case
        user_model = get_user_obj_perms_model(obj)
        related_name = user_model.user.field.related_query_name()
        if user_model.objects.is_generic():
            user_filters = {
                '%s__content_type' % related_name: ctype,
                '%s__object_pk' % related_name: obj.pk,
            }
        else:
            user_filters = {'%s__content_object' % related_name: obj}
        qset = Q(**user_filters)
        if only_with_perms_in is not None:
            permission_ids = Permission.objects.filter(content_type=ctype, codename__in=only_with_perms_in).values_list(
                'id', flat=True)
            qset &= Q(**{
                '%s__permission_id__in' % related_name: permission_ids,
            })
        if with_group_users:
            group_model = get_group_obj_perms_model(obj)
            if group_model.objects.is_generic():
                group_obj_perm_filters = {
                    'content_type': ctype,
                    'object_pk': obj.pk,
                }
            else:
                group_obj_perm_filters = {
                    'content_object': obj,
                }
            if only_with_perms_in is not None:
                group_obj_perm_filters.update({
                    'permission_id__in': permission_ids,
                })
            group_ids = set(
                group_model.objects.filter(**group_obj_perm_filters).values_list('group_id', flat=True).distinct())
            qset = qset | Q(groups__in=group_ids)
        if with_superusers:
            qset = qset | Q(is_superuser=True)

        model = get_user_obj_perms_model(obj)

        users = {}
        for user in get_user_model().objects.filter(qset).distinct():
            guardian_object = model.objects.get(user=user,
                                                object_pk=obj.pk,
                                                permission=40)
            users[user] = guardian_object.timestamp
        return users
    else:
        users = {}
        for user in get_users_timestamp_with_perms(obj,
                                                   with_group_users=with_group_users,
                                                   only_with_perms_in=only_with_perms_in,
                                                   with_superusers=with_superusers):
            if with_group_users or with_superusers:
                users[user] = sorted(get_perms(user, obj))
            else:
                users[user] = sorted(get_user_perms(user, obj))
        return users
