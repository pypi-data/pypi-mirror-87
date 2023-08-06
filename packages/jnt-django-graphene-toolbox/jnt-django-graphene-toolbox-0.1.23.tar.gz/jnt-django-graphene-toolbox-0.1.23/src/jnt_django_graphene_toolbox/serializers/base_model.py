from django.db import models
from jnt_django_toolbox.models.fields import EnumField as ModelEnumField
from rest_framework import serializers

from jnt_django_graphene_toolbox.serializers.fields import EnumField
from jnt_django_graphene_toolbox.serializers.fields.char import CharField


class ModelSerializer(serializers.ModelSerializer):
    """Base model serializer."""

    serializer_choice_field = EnumField

    def __init__(self, *args, **kwargs):
        """Init base model serializer, override fields."""
        self.serializer_field_mapping[models.CharField] = CharField
        self.serializer_field_mapping[models.TextField] = CharField
        super().__init__(*args, **kwargs)

    def build_standard_field(self, field_name, model_field):
        """Customize building standard field."""
        field_class, field_kwargs = super().build_standard_field(
            field_name, model_field,
        )
        if isinstance(model_field, ModelEnumField):
            field_kwargs.pop("choices", None)
            field_kwargs["enum"] = model_field.enum

        return field_class, field_kwargs
