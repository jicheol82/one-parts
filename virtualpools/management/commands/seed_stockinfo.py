import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User
from virtualpools.models import StockInfo, Stock

NAME = "stockinfos"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--n", default=1, type=int, help=f"How many {NAME} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("n")
        seeder = Seed.seeder()
        owner = User.objects.all()
        my_stock = Stock.objects.all()
        seeder.add_entity(
            StockInfo,
            number,
            {
                "owner": lambda x: random.choice(owner),
                "my_stock": lambda x: random.choice(my_stock),
                "num_stock": lambda x: random.randint(0, 100),
                "contact_person": lambda x: seeder.faker.name(),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
