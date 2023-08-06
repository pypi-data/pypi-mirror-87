import typing

from django_filters import FilterSet
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.filter.filterset import custom_filterset_factory

from jnt_django_graphene_toolbox.errors import GraphQLInputError

if typing.TYPE_CHECKING:
    _Base: DjangoFilterConnectionField
else:
    _Base = object


class ValidateFilterSetMixin(_Base):
    """Don't fail silently on filter set errors."""

    _filterset_class: FilterSet

    @property
    def filterset_class(self):
        """
        Initialising filterset_class.

        We remove here default django_graphene patching of filterset, because
        we don't use graphql GlobalId.
        """
        if self._filterset_class:
            return self._filterset_class

        elif self._provided_filterset_class:
            self._filterset_class = self._provided_filterset_class
            return self._filterset_class

        elif self.node_type._meta.filterset_class:  # noqa: WPS437
            self._filterset_class = (
                self.node_type._meta.filterset_class  # noqa: WPS437
            )
            return self._filterset_class

        self._filterset_class = self._generate_filter_set_class()
        return self._filterset_class

    @classmethod
    def resolve_queryset(  # noqa: WPS211
        cls,
        connection,
        iterable,
        info,  # noqa: WPS110
        args,
        filtering_args,
        filterset_class,
    ):
        """Resolve queryset."""
        filter_kwargs = {
            name: filter_
            for name, filter_ in args.items()
            if name in filtering_args
        }
        filterset = filterset_class(data=filter_kwargs)
        if not filterset.is_valid():
            raise GraphQLInputError(filterset.errors)

        return super().resolve_queryset(
            connection, iterable, info, args, filtering_args, filterset_class,
        )

    def _generate_filter_set_class(self) -> FilterSet:
        fields = (
            self._fields
            or self.node_type._meta.filter_fields  # noqa: WPS437, E501
        )
        meta = {"model": self.model, "fields": fields}
        if self._extra_filter_meta:
            meta.update(self._extra_filter_meta)

        return custom_filterset_factory(**meta)
