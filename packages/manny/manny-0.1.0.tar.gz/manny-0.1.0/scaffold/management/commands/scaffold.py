import os

from django.core.management.base import AppCommand

from scaffold.scaffold import Scaffold


class Command(AppCommand):
    def get_version(self):
        return f"scaffold 0.1"

    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = super(Command, self).create_parser(prog_name, subcommand)
        return parser

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "-m",
            "--model",
            dest="model",
            default=None,
            nargs="+",
            help="Add a new model with specific fields",
        )
        parser.add_argument(
            "-s",
            "--serializers",
            dest="serializers",
            default=None,
            nargs="*",
            help="Add a new serializer for the specific model or use keyword 'a' for all models",
        )
        parser.add_argument(
            "-u",
            "--urls",
            dest="urls",
            action="store_true",
            help="Add urls for all models",
        )
        parser.add_argument(
            "-vi",
            "--views",
            dest="views",
            default=None,
            nargs="*",
            help="Add a view for the specific model or use keyword 'a' for all models",
        )

    def handle_app_config(self, app_config, **options):
        settings = (
            options["settings"]
            if options.get("settings")
            else os.environ.get("DJANGO_SETTINGS_MODULE")
        )
        new_model = options["model"][0] if options.get("model") else None
        fields = options["model"][1:] if options.get("model") else None
        serializers = options.get("serializers", None)
        views = options.get("views")
        urls = options.get("urls", False)

        scaffold = Scaffold(
            proj_settings=settings,
            app_config=app_config,
            new_model=new_model,
            fields=fields,
            views=views,
            serializers=serializers,
            urls=urls,
        )
        scaffold.execute()
