import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users.models import Company, Domain, Branch

NAME = "Companies"


class Command(BaseCommand):

    help = "This command creates amenities"

    def add_arguments(self, parser):
        parser.add_argument(
            "--n", default=1, type=int, help=f"How many {NAME} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("n")
        seeder = Seed.seeder()
        branches = Branch.objects.all()
        seeder.add_entity(
            Company,
            number,
            {
                "name": lambda x: seeder.faker.company(),
            },
        )
        created_pk = seeder.execute()
        created_pk = flatten(list(created_pk.values()))

        for pk in created_pk:
            company = Company.objects.get(pk=pk)
            random_items = random.sample(
                list(branches), random.randint(1, len(branches))
            )
            company.branches.add(*random_items)
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
