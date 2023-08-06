import textwrap
from contextlib import contextmanager
from pathlib import Path

import toml
from graphql.type.definition import (
    GraphQLEnumType,
    GraphQLNonNull,
    GraphQLScalarType,
)

from .helpers import deep_get

gql_folder = Path(__file__).parent / "gql"


def first_item(dct):
    return list(dct.items())[0]


def node_is_terminal(obj):
    if isinstance(obj, (GraphQLNonNull)):
        return node_is_terminal(obj.of_type)
    elif isinstance(obj, (GraphQLScalarType, GraphQLEnumType)):
        return True
    else:
        return False


def generate_default_node(obj):

    keys = "\n".join(
        [key for key, field in obj.fields.items() if node_is_terminal(field.type)]
    )

    return "{\n" + keys + "\n}"


def generate_node(node_type):

    filename = gql_folder / (node_type.name + ".gql")

    if filename.exists():
        with open(filename) as f:
            return f.read()

    return generate_default_node(node_type)


def get_list_field_config(node_type):
    with open(gql_folder / "ListFields.toml") as f:
        list_fields = toml.load(f)
    default_fields = ["id", "name", "label", "description"]
    return list_fields.get(node_type, default_fields)


def format_node_from_dicts(node):
    if node:
        fields = "\n".join(
            [f"{key} {format_node_from_dicts(value)}" for key, value in node.items()]
        )
        return "{\n" + fields + "\n}\n"
    else:
        return ""


def generate_list_node(node_type):
    fields = get_list_field_config(node_type)
    node = {}

    for field in fields:
        parts = field.split(".")
        root = node
        stem, leaf = parts[:-1], parts[-1]
        for part in stem:
            if part not in root:
                root[part] = {}
            root = root[part]
        root[leaf] = None

    return format_node_from_dicts(node)


def filter_list_fields(result, node_type):
    fields = get_list_field_config(node_type)

    new_nodes = []
    for edge in result["edges"]:
        node = edge["node"]
        row = {}
        for field in fields:
            field_parts = field.split(".")
            if field_parts[0] in node:
                collapsed = node[field_parts[0]]
                row[field] = deep_get(collapsed, field_parts[1:])

        new_nodes.append(row)

    return new_nodes


class IndentWriter:
    """
    A simple utility to help with witing indented structures
    """

    def __init__(self):
        self.buffer = []
        self.level = 0

    @contextmanager
    def indent(self):
        self.increment()
        yield
        self.decrement()

    @contextmanager
    def space(self):
        self("")
        yield
        self("")

    def increment(self):
        self.level += 1

    def decrement(self):
        self.level -= 1

    def __call__(self, content):
        if isinstance(content, str):
            self([content])
        else:
            self.buffer.extend(["  " * self.level + line for line in content])

    def result(self):
        return "\n".join(self.buffer)


def format_graphql(call_type, args, field_name, node_path, node_gql):
    """
    Formats a graphQL statement based on its parts
    """

    wrt = IndentWriter()

    # Strips off the
    node_gql_body = textwrap.dedent(
        node_gql.strip().strip("{").strip("}").strip("\n")
    ).split("\n")

    wrt(f"{call_type}(")
    with wrt.indent():
        wrt([(f"${name}: {type}") for name, type in args])
    wrt(") {")

    with wrt.space():
        with wrt.indent():
            wrt(f"{field_name}(")
            with wrt.indent():
                wrt([(f"{name}: ${name}") for name, _ in args])
            wrt(") {")

            with wrt.indent():
                with wrt.space():
                    for part in node_path:
                        wrt(part + " {")
                        wrt.increment()

                    with wrt.space():
                        wrt(node_gql_body)

                    for part in node_path:
                        wrt.decrement()
                        wrt("}")
            wrt("}")
    wrt("}")

    result = wrt.result()
    return result


def generate_endpoint(call_type, client, field_name):

    if call_type == "mutation":
        root = client.schema.mutation_type
    elif call_type in ("retrieve", "list"):
        root = client.schema.query_type
    else:
        raise Exception("Unknown call type")

    root_field = root.fields[field_name]

    args = [(arg_name, str(arg.type)) for arg_name, arg in root_field.args.items()]

    field_type = root_field.type

    if call_type == "mutation":

        root_return_key, root_return_field = first_item(field_type.fields)
        root_return_type = root_return_field.type
        return_node = generate_node(root_return_type)
        return format_graphql(
            "mutation", args, field_name, [root_return_key], return_node
        )

    elif call_type == "retrieve":
        # Basically this gets us edges.node while going through
        # all the NonNull and List Shit
        root_return_type = (
            field_type.fields["edges"].type.of_type.of_type.fields["node"].type
        )
        return_node = generate_node(root_return_type)
        return format_graphql("query", args, field_name, ["edges", "node"], return_node)

    elif call_type == "list":
        # Basically this gets us edges.node while going through
        # all the NonNull and List Shit
        root_return_type = (
            field_type.fields["edges"].type.of_type.of_type.fields["node"].type
        )
        return_node = generate_list_node(root_return_type.name)

        return format_graphql("query", args, field_name, ["edges", "node"], return_node)
