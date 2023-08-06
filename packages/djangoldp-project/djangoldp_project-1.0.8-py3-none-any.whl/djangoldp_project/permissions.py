from djangoldp.permissions import LDPPermissions
from django.db.models.base import ModelBase
from djangoldp_project.xmpp import XMPP_SERVERS, get_client_ip
from djangoldp_project.filters import CustomerFilterBackend, ProjectFilterBackend, ProjectMemberFilterBackend


class CustomerPermissions(LDPPermissions):
    filter_backends=[CustomerFilterBackend]

    def user_permissions(self, user, obj_or_model, obj=None):
        from .models import Member

        if not isinstance(obj_or_model, ModelBase):
            obj = obj_or_model

        # start with the permissions set on the object and model
        perms = set(super().user_permissions(user, obj_or_model, obj))

        if not user.is_anonymous:
            # object-level permissions
            if obj and not isinstance(obj, ModelBase):
                # members of one of their projects can view the customer
                if Member.objects.filter(project__customer=obj, user=user).exists():
                    perms.add('view')

            # model-level permissions
            else:
                perms = perms.union({'view', 'add'})

        return list(perms)


class ProjectPermissions(LDPPermissions):
    filter_backends=[ProjectFilterBackend]

    def user_permissions(self, user, obj_or_model, obj=None):
        if not isinstance(obj_or_model, ModelBase):
            obj = obj_or_model

        # start with the permissions set on the object and model
        perms = set(super().user_permissions(user, obj_or_model, obj))

        if not user.is_anonymous:
            # object-level permissions
            if obj and not isinstance(obj, ModelBase):
                # permissions gained by being a member or an admin
                if obj.members.filter(user=user).exists():
                    perms.add('view')

                    if obj.members.filter(user=user).get().is_admin:
                        perms = perms.union({'add', 'change', 'delete'})

                # permissions gained by the project being public
                if obj.status == 'Public':
                    perms = perms.union({'view', 'add'})

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


class ProjectMemberPermissions(LDPPermissions):
    filter_backends = [ProjectMemberFilterBackend]

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

                    if not obj.is_admin or obj.project.members.filter(is_admin=True).count() > 1:
                        perms.add('delete')

                    if obj.project.status == 'Public':
                        perms = perms.union({'add', 'delete'})

                # the operation is on another user
                else:
                    # permissions gained in public circles
                    if obj.project.status == 'Public':
                        perms = perms.union({'view', 'add'})

                    # permissions gained for membership
                    if obj.project.members.filter(user=user).exists():
                        if obj.project.members.filter(user=user).get().is_admin:
                            perms = perms.union({'view', 'add'})

                            if not obj.is_admin:
                                perms.add('delete')
                        else:
                            perms.add('view')

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
