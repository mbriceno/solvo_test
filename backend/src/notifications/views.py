from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets

from .models import Notification
from .serializers import NotificationSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Notifications"],
        summary="List notifications",
        description="Returns a list of notifications for the authenticated user.",
    ),
    retrieve=extend_schema(
        tags=["Notifications"],
        summary="Get notification details",
    ),
    partial_update=extend_schema(
        tags=["Notifications"],
        summary="Mark notification as read",
        description="Allows updating the is_read status of a notification.",
    ),
)
class NotificationViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
