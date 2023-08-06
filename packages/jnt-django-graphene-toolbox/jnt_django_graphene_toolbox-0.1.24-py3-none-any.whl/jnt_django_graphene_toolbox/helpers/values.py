import json

from graphql import (
    GraphQLError,
    GraphQLNonNull,
    is_input_type,
    is_valid_value,
    print_ast,
    type_from_ast,
)
from graphql.execution.values import coerce_value


def get_variable_values(schema, definition_asts, inputs):
    """
    Monkey patch for graphql.

    Original: graphql/execution/values.py

    Prepares an object map of variables of the correct type based on
    the provided variable definitions and arbitrary input.
    If the input cannot be parsed to match the variable definitions,
    a GraphQLError will be thrown.
    """
    if inputs is None:
        inputs = {}

    values = {}  # type: ignore
    for def_ast in definition_asts:
        var_name = def_ast.variable.name.value
        var_type = type_from_ast(schema, def_ast.type)
        value = inputs.get(var_name)

        if not is_input_type(var_type):
            raise GraphQLError(
                'Variable "${var_name}" expected value of type "{var_type}"'
                " which cannot be used as an input type.".format(
                    var_name=var_name, var_type=print_ast(def_ast.type),
                ),
                [def_ast],
            )
        elif value is None:
            if isinstance(var_type, GraphQLNonNull):
                raise GraphQLError(
                    'Variable "${var_name}" of required type "{var_type}" '
                    "was not provided.".format(
                        var_name=var_name, var_type=var_type,
                    ),
                    [def_ast],
                )
            elif var_name in inputs:
                values[var_name] = value
        else:
            errors = is_valid_value(value, var_type)
            if errors:
                message = "\n{0}".format("\n".join(errors))
                raise GraphQLError(
                    'Variable "${0}" got invalid value {1}.{2}'.format(
                        var_name, json.dumps(value, sort_keys=True), message,
                    ),
                    [def_ast],
                )
            coerced_value = coerce_value(var_type, value)
            if coerced_value is None:
                raise Exception("Should have reported error.")

            values[var_name] = coerced_value

    return values
