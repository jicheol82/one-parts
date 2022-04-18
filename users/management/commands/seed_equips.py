import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import EquipGroup, Equipment

NAME = "Domains"


class Command(BaseCommand):

    help = "This command creates Domains"

    def add_arguments(self, parser):
        parser.add_argument(
            "--n", default=1, type=int, help=f"How many {NAME} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("n")
        eg = EquipGroup.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            Equipment,
            number,
            {
                "group": lambda x: random.choice(eg),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
