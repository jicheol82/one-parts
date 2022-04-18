from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import Branch

NAME = "Branches"


class Command(BaseCommand):

    help = "This command creates amenities"

    def add_arguments(self, parser):
        parser.add_argument(
            "--n", default=1, type=int, help=f"How many {NAME} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("n")
        seeder = Seed.seeder()
        seeder.add_entity(
            Branch,
            number,
            {
                "name": lambda x: seeder.faker.city(),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
