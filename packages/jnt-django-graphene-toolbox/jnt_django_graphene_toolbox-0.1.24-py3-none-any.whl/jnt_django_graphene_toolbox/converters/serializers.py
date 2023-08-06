import graphene
from graphene_django.rest_framework.serializer_converter import (
    convert_serializer_field_to_enum as base_convert_serializer_field_to_enum,
    get_graphene_type_from_serializer_field,
)
from graphene_file_upload.scalars import Upload
from rest_framework import serializers

from jnt_django_graphene_toolbox.converters.registry import get_registered_enum
from jnt_django_graphene_toolbox.serializers.fields import EnumField


@get_graphene_type_from_serializer_field.register(serializers.ManyRelatedField)
def convert_list_serializer_to_field(field):
    """Defines graphql field type for serializers.ManyRelatedField."""
    return (graphene.List, graphene.ID)


@get_graphene_type_from_serializer_field.register(
    serializers.PrimaryKeyRelatedField,
)
def convert_serializer_field_to_id(field):
    """Defines graphql field type for serializers.PrimaryKeyRelatedField."""
    return graphene.ID


@get_graphene_type_from_serializer_field.register(serializers.ImageField)
def convert_serializer_field_to_image(field):
    """Defines graphql field type for serializers.ImageField."""
    return Upload


@get_graphene_type_from_serializer_field.register(EnumField)
def convert_serializer_field_to_enum(field):
    """Convert serializers enum fields to rigth type."""
    registered = get_registered_enum(field.enum)
    if registered:
        return registered._meta.class_type  # noqa: WPS437

    return base_convert_serializer_field_to_enum(field)
