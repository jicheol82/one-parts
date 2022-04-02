from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import Domain


class Command(BaseCommand):

    help = "This command creates Domains"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many Domain you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            Domain,
            number,
            {
                "name": lambda x: "@" + seeder.faker.company_email().split("@")[1],
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} domains created!"))
