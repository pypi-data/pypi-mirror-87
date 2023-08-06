import json
import sys
import textwrap
from base64 import b64encode
from pathlib import Path

import toml
from graphql.error.syntax_error import GraphQLSyntaxError
from graphql.type.definition import (
    GraphQLEnumType,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLScalarType,
)
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import TOMLLexer, JsonLexer
from pygments_graphql import GraphqlLexer
from tabulate import tabulate
from termcolor import cprint

from gql import gql

from . import cleartoml
from .generate_gql import filter_list_fields, generate_endpoint
from .helpers import first_value


class CliException(Exception):
    """
    Exceptions thrown by the CLI
    """


gql_folder = Path(__file__).parent / "gql"


def pluralise_type(type):
    return type[0].lower() + type[1:] + "s"


def format_toml(value):
    return cleartoml.dumps(value)


def cell_output_for_table(value):
    if isinstance(value, dict):
        return json.dumps(value, indent=2)
    elif isinstance(value, list):
        return "\n".join(["- " + cell_output_for_table(child) for child in value])
    elif value is None:
        return ""
    else:
        return "\n".join(textwrap.wrap(str(value), 40))


def collapse_edges(value):

    if isinstance(value, list):
        return [collapse_edges(child) for child in value]

    if isinstance(value, dict):
        replacement = {}
        for key, child in value.items():

            if (
                isinstance(child, dict)
                and len(child) == 1
                and "edges" in child
                and isinstance(child["edges"], list)
            ):
                replacement[key] = [
                    collapse_edges(edge["node"]) for edge in child["edges"]
                ]
            else:
                replacement[key] = collapse_edges(child)
        return replacement
    else:
        return value


def format_for_terminal(value):
    code = format_toml(collapse_edges(value))
    if sys.stdout.isatty():
        return highlight(code, TOMLLexer(), TerminalFormatter())
    else:
        return code


def format_graphql_for_terminal(code):
    if sys.stdout.isatty():
        return highlight(code, GraphqlLexer(), TerminalFormatter())
    else:
        return code


def format_json_for_terminal(code):
    if sys.stdout.isatty():
        return highlight(code, JsonLexer(), TerminalFormatter())
    else:
        return code


def format_table_for_terminal(nodes):
    nodes = collapse_edges(nodes)
    if nodes:
        columns = nodes[0].keys()
        headers = [key.replace(".", "\n") for key in columns]
        rows = [
            [cell_output_for_table(node.get(key)) for key in columns] for node in nodes
        ]
        return tabulate(rows, headers=headers, tablefmt="fancy_grid")

    else:
        return f"No matching items"


class Rely:
    def __init__(self, client, typ, action, filename=None, **kwargs):
        self.client = client
        self.type = typ
        self.action = action
        self.filename = filename
        self.kwargs = kwargs

        # A list of all the queries that have been executed
        self.execution_log = []

    def act(self):
        if self.type.lower() == "mutation":
            return self.general_mutation()
        elif self.action == "retrieve":
            return self.retrieve()
        elif self.action == "list":
            return self.list()
        elif self.action == "template":
            return self.template()
        elif self.action == "delete":
            return self.delete()
        else:
            return self.crud_mutation()

    def _execute(self, graphql, wrap_variables=False):
        try:
            query = gql(graphql)
        except GraphQLSyntaxError:
            output_error("[Bad GraphQL Error]")
            output_error(graphql)
            sys.exit(1)

        variable_values = self.kwargs
        if self.filename:
            with open(self.filename) as f:
                variable_values = {**toml.load(f), **variable_values}

        for key in list(variable_values):
            if key[0] == "@":
                new_key = key[1:]
                value = variable_values.pop(key)
                with open(value, "rb") as f:
                    new_value = b64encode(f.read()).decode("ascii")
                variable_values[new_key] = new_value

        if wrap_variables:
            variable_values = {"input": variable_values}

        self.execution_log.append((graphql, variable_values))
        return self.client.execute(query, variable_values=variable_values)

    def get_type_mutation_name(self, action=None):
        action = action or self.action

        with open(gql_folder / "aliases.toml") as f:
            alias_mappings = toml.load(f)

        mutations = self.client.schema.mutation_type.fields

        aliases = [
            *(
                (alias_action + alias_type, mutation_name)
                for alias_type, alias_actions in alias_mappings.items()
                for alias_action, mutation_name in alias_actions.items()
            ),
            *((mutation_name, mutation_name) for mutation_name in mutations.keys()),
        ]

        given_name = (action + self.type).lower()
        for alias, mutation_name in aliases:
            if alias.lower() == given_name:
                return mutation_name

        # Find all the possible mutations
        possible_actions = [
            mutation_name[: -len(self.type.lower())]
            for _, mutation_name in aliases
            if mutation_name.lower().endswith(self.type.lower())
        ]

        # See if maybe it can be queried
        if self.get_query_name_and_type():
            possible_actions.extend(["retrieve", "list"])

        if possible_actions:
            message = f"Action '{self.action}' not recognised for type '{self.type}', possible actions are:\n"
            raise CliException(
                message + "\n".join([f"  - {action}" for action in possible_actions])
            )
        else:
            raise CliException(f"Type '{self.type}' is not recognised")

    def get_query_name_and_type(self):
        plural_name_lower = pluralise_type(self.type).lower()
        query_keys = {
            key: value for key, value in self.client.schema.query_type.fields.items()
        }

        for query_key, field in query_keys.items():
            if plural_name_lower == query_key.lower():
                query_type = (
                    field.type.fields["edges"].type.of_type.of_type.fields["node"].type
                )
                return query_key, query_type.name

        return None

    def check_query_name_and_type(self):
        query_name_and_type = self.get_query_name_and_type()
        if not query_name_and_type:
            raise CliException(f"Query type '{self.type}' not recognised.")
        return query_name_and_type

    def crud_mutation(self):

        operation_name = self.get_type_mutation_name()

        graphql = generate_endpoint("mutation", self.client, operation_name)

        gql_result = self._execute(graphql, wrap_variables=True)

        result = gql_result[operation_name]

        return first_value(result)

    def general_mutation(self):
        graphql = generate_endpoint("mutation", self.client, self.action)
        gql_result = self._execute(graphql, wrap_variables=True)
        return first_value(first_value(gql_result))

    def retrieve(self):
        query_key, _ = self.check_query_name_and_type()
        graphql = generate_endpoint("retrieve", self.client, query_key)
        gql_result = self._execute(graphql)
        result = first_value(gql_result)

        edges = result["edges"]

        if len(edges) == 1:
            return edges[0]["node"]
        elif len(edges) == 0:
            raise CliException(f"No matching {self.type} found")
        else:
            raise CliException(f"Multiple matching {self.type} items found")

    def list(self):
        query_key, query_type = self.check_query_name_and_type()
        graphql = generate_endpoint("list", self.client, query_key)
        gql_result = self._execute(graphql)
        result = first_value(gql_result)
        return filter_list_fields(result, query_type)

    def delete(self):
        mutation_name = self.get_type_mutation_name()
        graphql = textwrap.dedent(
            f"""
            mutation($id: ID!) {{
              {mutation_name}(input: {{
                id: $id
              }}) {{
                ok
              }}
            }}
            """
        )
        return self._execute(graphql)

    def template(self):
        operation_name = self.get_type_mutation_name("create")
        schema = self.client.schema
        payload = schema.mutation_type.fields[operation_name].args["input"].type.of_type

        template = gql_type_to_template(payload)
        del template["clientMutationId"]

        if "from" in self.kwargs:
            from_id = self.kwargs["from"]

            # Basically for a given createXYZ mutation we need to find the correct thing to query
            # There is a loose name based mapping but this is a little brittle
            # We probably need a way to rigourously define the object model
            # That can be doen in the future
            primary_types = [
                key[:-1].lower() for key in schema.query_type.fields.keys()
            ]
            possible_types = [
                key for key in primary_types if operation_name.lower().endswith(key)
            ]
            if len(possible_types) != 1:
                raise Exception(
                    f"Matching query type could not be found for {operation_name}"
                )

            from_type = possible_types[0]
            from_object = collapse_edges(
                Rely(self.client, from_type, "retrieve", id=from_id).act()
            )

            return fill_in_template(template, from_object)
        else:
            return template


def gql_type_to_template(obj):
    if isinstance(obj, GraphQLInputObjectType):
        return {k: gql_type_to_template(v) for k, v in obj.fields.items()}
    elif isinstance(obj, GraphQLInputField):
        return gql_type_to_template(obj.type)
    elif isinstance(obj, GraphQLList):
        return [gql_type_to_template(obj.of_type)]
    elif isinstance(obj, GraphQLNonNull):
        return gql_type_to_template(obj.of_type)
    elif isinstance(obj, GraphQLScalarType):
        return obj.name
    elif isinstance(obj, GraphQLEnumType):
        return "|".join([value for value in obj.values])
    else:
        raise CliException(f"Unknown type to template {obj}")


def fill_in_template(template, obj):
    """
    Given a create template and an existing object, this will fill in the template with all the matching
    values from the object.
    """

    if obj is None:
        return template
    elif isinstance(template, dict):
        return {k: fill_in_template(template[k], obj.get(k)) for k in template}
    elif isinstance(template, list):
        return [fill_in_template(template[0], obj_child) for obj_child in obj]
    else:
        if isinstance(obj, dict):
            if "name" in obj:
                return obj["name"]
            elif "id" in obj:
                return obj["id"]
            else:
                return template

        return obj


def output_error(message):
    cprint(message, "red", file=sys.stderr)
