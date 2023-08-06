import argparse
import json
from pathlib import Path
import textwrap

import requests
import toml

from gql import Client
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport

from .rely import (
    CliException,
    Rely,
    format_for_terminal,
    format_graphql_for_terminal,
    format_json_for_terminal,
    format_table_for_terminal,
    output_error,
)


def check_auth(email, password, url, impersonate):
    pass


class GqlClientConnectionError(Exception):
    def __init__(self, body):
        super().__init__(body["errors"][0]["message"])
        self.body = body


def gql_client(email, password, url, impersonate):
    transport = RequestsHTTPTransport(
        url=url,
        verify=True,
        retries=3,
        auth=(email, password),
        headers={"IMPERSONATE": impersonate},
    )
    try:
        return Client(transport=transport, fetch_schema_from_transport=True)
    except Exception:
        # Probably an authorisation error
        response = requests.post(
            url, auth=(email, password), headers={"IMPERSONATE": impersonate}
        )

        try:
            body = response.json()
        except:
            body = {
                "errors": [
                    {"message": f"Unknown error, status code {response.status_code}"}
                ]
            }

        raise GqlClientConnectionError(body)


def main():

    # Lookup config from config file
    config = {}

    folders = [Path(".").resolve()]
    while folders[-1] != Path("/"):
        folders.append(folders[-1].parent)

    for folder in folders:
        config_path = folder / ".rely.toml"
        if config_path.exists():
            with open(config_path, "r") as f:
                config = toml.load(f)
            break

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="A command line interface for the RelyComply platform",
        epilog=textwrap.dedent(
            """
            Additional keyword arguments can be passed through to the RelyComply platform 
            in the form '--key=value'. 

            If the final argument is a file path it will attempt to load the file as a 
            TOML file. The additional keyword arguments are merged with the values of 
            the input TOML file. The command line arguments will take precedence.

            For more information please see https://docs.relycomply.com.
            """
        ),
    )
    parser.add_argument("type", help="the type of object to perform an action on")
    parser.add_argument("action", help="the action to perform")

    # Auth arguments
    parser.add_argument(
        "--auth",
        default=config.get("auth"),
        help="the auth details in the form email:password",
    )
    parser.add_argument(
        "--host",
        default=config.get("host") or "https://app.relycomply.com/graphql/",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--impersonate", default=config.get("impersonate"), help=argparse.SUPPRESS
    )

    # Explain the graphql instructions
    parser.add_argument(
        "--explain",
        action="store_true",
        help="print out an explanation of the GraphQL commands executed",
    )

    # TODO: Implement this
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument("--toml", action="store_true")
    # group.add_argument("--json", action="store_true")
    # group.add_argument("--yaml", action="store_true")
    # group.add_argument("--csv", action="store_true")

    set_args, other_args = parser.parse_known_args()

    try:
        if not set_args.auth:
            raise CliException("No auth details found")

        if set_args.auth.count(":") != 1:
            raise CliException(
                "Incorrect auth format. Auth details must be of the form '<email>:<password>'."
            )

        email, password = set_args.auth.split(":")

        try:
            client = gql_client(
                email,
                password,
                url=set_args.host,
                impersonate=set_args.impersonate,
            )
        except GqlClientConnectionError as e:
            raise CliException(str(e))

        action = set_args.action

        kwargs = [part for part in other_args if part.startswith("--")]

        try:
            kwargs = dict(part[2:].split("=", 1) for part in kwargs)
        except ValueError:
            raise CliException(
                "Keyword arguments must be of the form '--<key>=<value>'."
            )

        straight_args = [part for part in other_args if not part.startswith("--")]

        if not straight_args:
            filename = None
        elif len(straight_args) == 1:
            filename = straight_args[0]
        else:
            raise CliException("Too many input filename arguments")

        kwargs["filename"] = filename

        rely = Rely(client, set_args.type, action, **kwargs)
        result = rely.act()

        if set_args.explain:
            for execution in rely.execution_log:
                execution_gql, execution_variables = execution
                print("GraphQL:\n")
                print(format_graphql_for_terminal(execution_gql))
                print("\nVariables:\n")
                print(
                    format_json_for_terminal(json.dumps(execution_variables, indent=2))
                )
                print("\nOutput:\n")

        if action == "list":
            output = format_table_for_terminal
        else:
            output = format_for_terminal

        print(output(result))

    except TransportQueryError as e:
        output_error("[Error]")
        packet = eval(str(e))
        output_error(packet["message"])
        exit(1)

    except CliException as e:
        output_error("[Command Line Exception]")
        output_error(e)
        exit(1)


if __name__ == "__main__":
    main()
