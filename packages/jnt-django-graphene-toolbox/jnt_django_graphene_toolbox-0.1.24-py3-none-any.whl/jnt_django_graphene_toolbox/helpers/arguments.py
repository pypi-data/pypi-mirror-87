from graphene.types import argument
from graphene_django.filter.utils import get_filtering_args_from_filterset


def from_filterset(filterset_class):
    """Converts filterset fields to graphql arguments."""
    return argument.to_arguments(
        get_filtering_args_from_filterset(filterset_class, None),
    )
