from typing import Any, Dict, List, Optional, Sequence

from django.utils.translation import gettext_lazy as _
from graphene_django.utils import camelize

from jnt_django_graphene_toolbox.errors.base import BaseGraphQLError

INPUT_ERROR = "INPUT_ERROR"


class GraphQLInputError(BaseGraphQLError):
    """Input error - should be used for mutation errors."""

    _default_message: str = _("Input error")
    _default_extensions: Optional[Dict[str, str]] = {
        "code": INPUT_ERROR,
    }

    def __init__(self, errors, extensions=None, *args, **kwargs) -> None:
        """Init input error with serializer errors."""
        if not extensions:
            extensions = {}

        extensions["fieldErrors"] = self._convert_errors(errors)
        kwargs["extensions"] = extensions

        super().__init__(*args, **kwargs)

    def _convert_errors(  # type: ignore
        self, errors, index=None,
    ) -> Sequence[Any]:
        field_errors = []

        for field, messages in camelize(errors).items():
            error_obj = {
                "fieldName": field,
                "messages": self._get_converted_err_messages(messages),
            }
            if index is not None:
                error_obj["index"] = index

            field_errors.append(error_obj)

        return field_errors

    def _get_converted_err_messages(  # type: ignore
        self, messages,
    ) -> Sequence[Any]:
        converted_msgs: List[Any] = []  # type: ignore

        if isinstance(messages, dict):
            return self._convert_errors(messages)

        for index, message in enumerate(messages):
            if not message:
                continue

            if isinstance(message, dict):
                converted_msgs.extend(self._convert_errors(message, index))

            else:
                converted_msgs.append(message)

        return converted_msgs
