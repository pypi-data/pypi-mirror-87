from typing import Dict, Type, Union

from django.forms import Form
from graphql import ResolveInfo
from rest_framework.exceptions import ValidationError

from jnt_django_graphene_toolbox.mutations import BaseMutation


class ArgumentsValidationMixin:
    """A Mixin validates input fields in mutations."""

    form_class: Type[Form]

    @classmethod
    def do_mutate(
        cls: Union["ArgumentsValidationMixin", BaseMutation],
        root,
        info,  # noqa: WPS110
        **kwargs,
    ):
        """Do mutate."""
        form = cls.form_class(data=kwargs)

        if not form.is_valid():
            raise ValidationError(form.errors)

        return cls.perform_mutate(info, form.cleaned_data)

    @classmethod
    def perform_mutate(
        cls,
        info: ResolveInfo,  # noqa: WPS110
        cleaned_data: Dict[str, object],
    ) -> None:
        """Method should be implemente in subclass."""
        raise NotImplementedError
