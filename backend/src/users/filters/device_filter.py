from typing import Final

import django_filters

from users.models import Device


class DeviceFilter(django_filters.FilterSet):

    class Meta:
        model = Device
        fields: Final[dict] = {
            "is_active": ["exact"],
            "last_seen": ["gte", "lte"],
            "name": ["icontains"],
            "ip_address": ["icontains"],
        }
