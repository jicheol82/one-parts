from django.core.management.base import BaseCommand
from users.models import EquipGroup

NAME = "equipment groups"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def handle(self, *args, **options):
        # csv 파일을 이용하여 바꾸는 방법은?
        equip_groups = [
            "Gas turbine",
            "Steam turbine",
            "HRSG",
            "Generator",
            "AVR",
            "SFC",
            "Exciter",
            "Gas compressor",
            "Condenser",
            "Boiler",
            "Auxilary boiler",
        ]

        for i in equip_groups:
            EquipGroup.objects.create(name=i)
        self.stdout.write(self.style.SUCCESS(f"{len(equip_groups)} {NAME} created!"))
