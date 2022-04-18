import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import Domain, Company

NAME = "domains"


class Command(BaseCommand):

    help = "This command creates Domains"

    def add_arguments(self, parser):
        parser.add_argument(
            "--n", default=1, type=int, help="How many {NAME} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("n")
        companies = Company.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            Domain,
            number,
            {
                "name": lambda x: seeder.faker.company_email().split("@")[1],
                "company": lambda x: random.choice(companies),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
