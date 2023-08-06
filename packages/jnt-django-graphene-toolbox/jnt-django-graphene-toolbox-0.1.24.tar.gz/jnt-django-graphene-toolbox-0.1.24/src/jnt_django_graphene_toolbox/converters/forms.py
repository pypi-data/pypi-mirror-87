import graphene
from graphene import List
from graphene_django.forms.converter import (
    convert_form_field,
    convert_form_field_to_string,
)
from jnt_django_toolbox.forms.fields import (
    EnumChoiceField,
    MultipleEnumChoiceField,
)

from jnt_django_graphene_toolbox.converters.registry import get_registered_enum
from jnt_django_graphene_toolbox.filters.integers_array import (
    IntegersArrayField,
)
from jnt_django_graphene_toolbox.filters.strings_array import StringsArrayField


@convert_form_field.register(IntegersArrayField)
def convert_integers_array_field(field):
    """Convert form field."""
    return graphene.List(graphene.ID)


@convert_form_field.register(StringsArrayField)
def convert_strings_array_field(field):
    """Convert form field."""
    return graphene.List(graphene.String)


@convert_form_field.register(EnumChoiceField)
def convert_choice_field(field):
    """Convert form field."""
    registered = get_registered_enum(field.enum)
    if registered:
        return registered._meta.class_type(  # noqa: WPS437
            required=field.required,
        )

    return convert_form_field_to_string(field)


@convert_form_field.register(MultipleEnumChoiceField)
def convert_multiple_enum_choice_field(field):
    """Convert form field."""
    return List(graphene.Enum.from_enum(field.enum), required=field.required)
