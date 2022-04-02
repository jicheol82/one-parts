import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users.models import Equipment, User, Company


class Command(BaseCommand):

    help = "This command creates amenities"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        companies = Company.objects.all()
        equipments = Equipment.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
                "contact_number": lambda x: seeder.faker.phone_number(),
                "company_email": lambda x: seeder.faker.company_email(),
                "my_company": lambda x: random.choice(companies),
            },
        )
        created_pk = seeder.execute()
        created_pk = flatten(list(created_pk.values()))
        for pk in created_pk:
            user = User.objects.get(pk=pk)
            random_items = random.sample(
                list(equipments), random.randint(1, len(equipments))
            )
            user.interesting_equips.add(*random_items)

        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
