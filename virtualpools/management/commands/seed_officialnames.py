from django.core.management.base import BaseCommand
from django_seed import Seed
from virtualpools.models import OfficialMakerName

NAME = "official company nemes"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--n", default=1, type=int, help=f"How many {NAME} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("n")
        seeder = Seed.seeder()
        seeder.add_entity(
            OfficialMakerName,
            number,
            {
                "name": lambda x: seeder.faker.company(),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME}created!"))
