from django.core.management.base import BaseCommand

# from django_seed import Seed
from users.models import EquipGroup


class Command(BaseCommand):

    help = "This command creates Equipment group"

    def handle(self, *args, **options):
        # csv 파일을 이용하여 바꾸는 방법은?
        equip_groups = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        for i in equip_groups:
            EquipGroup.objects.create(name=i)
        self.stdout.write(
            self.style.SUCCESS(f"{len(equip_groups)} equipment groups created!")
        )
