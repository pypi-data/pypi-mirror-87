import graphene
from django.db import models
from graphene_django.converter import convert_django_field
from jnt_django_toolbox.models.fields import BitField as ModelBitField

from jnt_django_graphene_toolbox.types import BitField, ImageType


@convert_django_field.register(ModelBitField)
def convert_bit_field(field, registry=None):
    """Field to float."""
    return graphene.Field(
        BitField, description=field.help_text, required=not field.null,
    )


@convert_django_field.register(models.ImageField)
def convert_image_field(field, registry=None):
    """Register handler for image fields."""
    return ImageType()
