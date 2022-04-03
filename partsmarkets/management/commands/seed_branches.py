from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import Branch


class Command(BaseCommand):

    help = "This command creates amenities"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            Branch,
            number,
            {
                "name": lambda x: seeder.faker.city(),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} branches created!"))
