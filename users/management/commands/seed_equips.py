import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import EquipGroup, Equipment


class Command(BaseCommand):

    help = "This command creates Domains"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many Domain you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        eg = EquipGroup.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            Equipment,
            number,
            {
                "equipment_group": lambda x: random.choice(eg),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} domains created!"))
