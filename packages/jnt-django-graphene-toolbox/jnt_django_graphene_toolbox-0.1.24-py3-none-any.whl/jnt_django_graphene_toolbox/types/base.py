from graphene_django import DjangoObjectType
from graphene_django.registry import get_global_registry
from jnt_django_toolbox.models.fields import EnumField

from jnt_django_graphene_toolbox.security.mixins.node import AuthNode
from jnt_django_graphene_toolbox.security.permissions import AllowAuthenticated


class BaseDjangoObjectType(AuthNode, DjangoObjectType):
    """A base class Django object type."""

    class Meta:
        abstract = True

    permission_classes = (AllowAuthenticated,)

    @classmethod
    def __init_subclass_with_meta__(cls, *args, **kwargs):
        super().__init_subclass_with_meta__(*args, **kwargs)

        cls._update_enums_in_global_registry()

    @classmethod
    def _update_enums_in_global_registry(cls) -> None:
        global_registry = get_global_registry()
        enum_fields = [
            field
            for field in cls._meta.model._meta.get_fields()  # noqa: WPS437
            if isinstance(field, EnumField)
        ]

        for field in enum_fields:
            converted = global_registry.get_converted_field(field)
            if converted:
                converted.django_enum = field.enum
