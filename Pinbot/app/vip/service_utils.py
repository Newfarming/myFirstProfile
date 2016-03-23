# coding: utf-8

from django.contrib.contenttypes.models import ContentType

from .models import (
    ItemRecord,
)
from .models import (
    UserManualService
)
from pin_utils.django_utils import (
    get_object_or_none
)


class ServiceUtils(object):

    @classmethod
    def get_service_order(cls, service):
        service_model = service.__class__
        content_type = ContentType.objects.get_for_model(service_model)

        order_items_query = ItemRecord.objects.select_related(
            'order',
        ).filter(
            item_content_type=content_type,
            item_object_id=service.id,
        )
        if not order_items_query:
            return None
        order = order_items_query[0].order
        return order

    @classmethod
    def get_order_by_manual_serviceid(cls, service_id):
        service = get_object_or_none(
            UserManualService,
            id=service_id,
        )
        return cls.get_service_order(service=service)

