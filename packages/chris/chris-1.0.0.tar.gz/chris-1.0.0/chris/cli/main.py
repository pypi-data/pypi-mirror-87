"""Main entrypoint for the chris package."""
import argparse

from chris.app.app import App
from chris.validation.projects.project_validator import validate as validate_projects
from chris.validation.posts.post_validator import validate as validate_posts


SUBPARSER_NAME_APP = 'app'
SUBPARSER_NAME_VALIDATE = 'validate'


def start_app():
    """Start a webserver and run the app."""
    App().run()


def parse_args():
    """Parse script args."""
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(required=True, dest='command',
                                       help="Chris package commands.")

    subparsers.add_parser(SUBPARSER_NAME_APP)
    subparsers.add_parser(SUBPARSER_NAME_VALIDATE)

    args = parser.parse_args()
    return args


def run_cli():
    """Run the package CLI."""
    args = parse_args()

    if args.command == SUBPARSER_NAME_APP:
        start_app()
    elif args.command == SUBPARSER_NAME_VALIDATE:
        validate_posts()
        validate_projects()
    else:
        raise ValueError("Invalid command")
