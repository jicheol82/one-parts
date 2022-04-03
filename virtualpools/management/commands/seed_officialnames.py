from django.core.management.base import BaseCommand
from django_seed import Seed
from virtualpools.models import OfficialMakerName

TITLE = "official names"


class Command(BaseCommand):

    help = f"This command creates {TITLE}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help=f"How many {TITLE} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            OfficialMakerName,
            number,
            {
                "name": lambda x: seeder.faker.company(),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} {TITLE}created!"))
