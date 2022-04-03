import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from virtualpools.models import OtherMakerName, OfficialMakerName


TITLE = "company names"


class Command(BaseCommand):
    help = f"This command creates {TITLE}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help=f"How many {TITLE} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        official_names = OfficialMakerName.objects.all()
        seeder.add_entity(
            OtherMakerName,
            number,
            {
                "name": lambda x: seeder.faker.company(),
                "official_name": lambda x: random.choice(official_names),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {TITLE} created!"))
