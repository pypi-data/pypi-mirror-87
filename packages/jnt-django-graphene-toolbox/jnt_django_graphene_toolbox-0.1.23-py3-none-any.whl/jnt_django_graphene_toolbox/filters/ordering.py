from django_filters import OrderingFilter as BaseOrderingFilter

from jnt_django_graphene_toolbox.filters.mixins import CamelCasedOrderingMixin

BASE_COLLECTION_ORDER_FIELD = "order"


class OrderingFilter(CamelCasedOrderingMixin, BaseOrderingFilter):
    """Ordering filter."""


class BaseCollectionOrderingFilter(OrderingFilter):
    """Default ordering filter for base collection items."""

    def __init__(self, *args, **kwargs):
        """Init BaseCollectionOrderingFilter."""
        self._add_order_to_fields(kwargs)
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):  # noqa: WPS110,WPS125
        """Filter queryset."""
        return super().filter(qs, value or [BASE_COLLECTION_ORDER_FIELD])

    def _add_order_to_fields(self, kwargs) -> None:
        if "fields" not in kwargs:
            kwargs["fields"] = (BASE_COLLECTION_ORDER_FIELD,)
        elif BASE_COLLECTION_ORDER_FIELD not in kwargs["fields"]:
            kwargs["fields"] = (BASE_COLLECTION_ORDER_FIELD, *kwargs["fields"])
