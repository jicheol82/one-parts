import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users.models import Branch, Domain, Equipment, User, Company

NAME = "users"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--n", default=1, type=int, help=f"How many {NAME} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("n")
        companies = Company.objects.all()
        branches = Branch.objects.all()
        domains = Domain.objects.all()
        equipments = Equipment.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
                "email": lambda x: seeder.faker.company_email(),
                "company": lambda x: random.choice(companies),
                "branch": lambda x: random.choice(branches),
                "is_verified": lambda x: random.randint(0, 1),
                "token": "",
            },
        )
        created_pk = seeder.execute()
        created_pk = flatten(list(created_pk.values()))
        for pk in created_pk:
            user = User.objects.get(pk=pk)
            random_items = random.sample(
                list(equipments), random.randint(1, len(equipments))
            )
            user.my_equips.add(*random_items)

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
