import os

from django.core.management.base import BaseCommand

from scaffold.scaffold import ScaffoldApp


class Command(BaseCommand):
    def get_version(self):
        return f"scaffold 0.1"

    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = super(Command, self).create_parser(prog_name, subcommand)
        return parser

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument("new_apps", nargs="*", help="Add new apps")

    def handle(self, *args, **options):
        if not options.get("new_apps"):
            SystemExit("Provide app name...")
        new_apps = options.get("new_apps")
        settings = (
            options["settings"]
            if options.get("settings")
            else os.environ.get("DJANGO_SETTINGS_MODULE")
        )
        scaffold = ScaffoldApp(settings, new_apps)
        scaffold.execute()
