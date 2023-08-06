from django.db.models import Q
from djangoldp.filters import LDPPermissionsFilterBackend
from djangoldp_project.xmpp import get_client_ip, XMPP_SERVERS


class CustomerFilterBackend(LDPPermissionsFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_anonymous:
            return super().filter_queryset(request, queryset, view)
        else:
            return queryset.filter(project__members__user=request.user)


class ProjectFilterBackend(LDPPermissionsFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if get_client_ip(request) in XMPP_SERVERS:
            return queryset
        elif request.user.is_anonymous:
            return queryset.filter(status='Public')
        else:
            return queryset.filter(
                Q(members__user=request.user) |
                Q(status='Public')).distinct()


class ProjectMemberFilterBackend(LDPPermissionsFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if get_client_ip(request) in XMPP_SERVERS:
            return queryset
        elif request.user.is_anonymous:
            return super().filter_queryset(request, queryset, view)
        else:
            return super().filter_queryset(request, queryset, view).filter(
                Q(user=request.user) |
                Q(project__status='Public') |
                Q(project__members__user=request.user)).distinct()
