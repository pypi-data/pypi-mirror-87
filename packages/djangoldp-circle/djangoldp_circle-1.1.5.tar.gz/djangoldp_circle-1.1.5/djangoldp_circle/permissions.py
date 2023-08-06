from django.conf import settings
from django.db.models import QuerySet, Q
from django.db.models.base import ModelBase

from djangoldp.permissions import LDPPermissions
from djangoldp_circle.filters import CircleFilterBackend, CircleMemberFilterBackend
from djangoldp_circle.xmpp import get_client_ip, XMPP_SERVERS


def _append_circle_object_permissions(perms, obj, user):
    '''Auxiliary function analyses a circle object for member permissions'''
    # permissions gained by being a circle-member, and admin
    if obj.members.filter(user=user).exists():
        perms = perms.union({'view', 'add'})

        if obj.members.filter(user=user).get().is_admin:
            perms = perms.union({'change', 'delete'})

    # permissions gained by the circle being public
    if obj.status == 'Public':
        perms = perms.union({'view', 'add'})

    return perms


class CirclePermissions(LDPPermissions):
    filter_backends = [CircleFilterBackend]

    def user_permissions(self, user, obj_or_model, obj=None):
        if not isinstance(obj_or_model, ModelBase):
            obj = obj_or_model

        # start with the permissions set on the object and model
        perms = set(super().user_permissions(user, obj_or_model, obj))

        if not user.is_anonymous:
            # object-level permissions
            if obj and not isinstance(obj, ModelBase):
                perms = _append_circle_object_permissions(perms, obj, user)

            # model-level permissions
            else:
                perms = perms.union({'view', 'add'})

        return list(perms)
    
    def has_permission(self, request, view):
        if get_client_ip(request) in XMPP_SERVERS:
            return True

        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        if get_client_ip(request) in XMPP_SERVERS:
            return True

        return super().has_object_permission(request, view, obj)


class CircleMemberPermissions(LDPPermissions):
    filter_backends = [CircleMemberFilterBackend]

    def user_permissions(self, user, obj_or_model, obj=None):
        if not isinstance(obj_or_model, ModelBase):
            obj = obj_or_model

        # start with the permissions set on the object and model
        perms = set(super().user_permissions(user, obj_or_model, obj))

        if not user.is_anonymous:
            # object-level permissions
            if obj and hasattr(obj, 'user') and not isinstance(obj, ModelBase):
                # the operation is on myself
                if obj.user == user:
                    perms.add('view')

                    if not obj.is_admin or obj.circle.members.filter(is_admin=True).count() > 1:
                        perms.add('delete')

                    if obj.circle.status == 'Public':
                        perms = perms.union({'add', 'delete'})

                # the operation is on another member
                else:
                    # permissions gained in public circles
                    if obj.circle.status == 'Public':
                        perms = perms.union({'view', 'add'})

                    # permissions gained for all members
                    if obj.circle.members.filter(user=user).exists():
                        perms = perms.union({'view', 'add'})

                        # permissions gained for admins (on other users)
                        if obj.circle.members.filter(user=user).get().is_admin \
                                and not obj.is_admin:
                            perms = perms.union({'delete', 'change'})

            # model-level permissions
            # NOTE: if the request is made on a nested field, this could be the parent container object and model
            # in our case, circle or the user model
            else:
                if obj is not None:
                    if hasattr(obj, 'members'):
                        perms = _append_circle_object_permissions(perms, obj, user)

        return list(perms)
    
    def has_permission(self, request, view):
        if get_client_ip(request) in XMPP_SERVERS:
            return True

        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        if get_client_ip(request) in XMPP_SERVERS:
            return True

        return super().has_object_permission(request, view, obj)
