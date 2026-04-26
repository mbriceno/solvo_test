from core.pagination import CustomPagination
from django.http import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from platforms.rule_resolver import RuleResolver
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from users.filters import DeviceFilter
from users.repositories import DeviceRepository
from users.services import DeviceService

from .serializers import DeviceSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Devices"],
        summary="List devices",
        description=(
            "Returns a paginated list of devices registered "
            "by the authenticated user. Results are automatically "
            "filtered by the platform authenticated in the Bearer token."
        ),
    ),
    create=extend_schema(
        tags=["Devices"],
        summary="Register device",
        description=(
            "Registers a new device for the user, "
            "subject to platform rule validation."
        ),
    ),
    retrieve=extend_schema(tags=["Devices"], summary="Get device details"),
    update=extend_schema(tags=["Devices"], summary="Update device details"),
    partial_update=extend_schema(
        tags=["Devices"], summary="Partially update device details",
    ),
    destroy=extend_schema(tags=["Devices"], summary="Remove device"),
)
class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DeviceFilter

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return DeviceRepository.model.objects.none()

        service = DeviceService(DeviceRepository(), RuleResolver())
        return service.get_devices_for_user_on_platform(
            user=self.request.user,
            platform=self.request.user.platform,
        )

    def create(self, request: HttpRequest, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = DeviceService(DeviceRepository(), RuleResolver())
        try:
            device = service.register_device(
                user=request.user,
                platform=request.user.platform,
                name=serializer.validated_data["name"],
                ip_address=serializer.validated_data["ip_address"],
            )
            return Response(
                DeviceSerializer(device).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN,
            )
