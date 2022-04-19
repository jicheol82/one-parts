import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from partsmarkets.models import Product, Photo
from users.models import User, EquipGroup
from virtualpools.models import OfficialMakerName

NAME = "products"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--n", default=1, type=int, help=f"How many {NAME} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("n")
        seeder = Seed.seeder()
        sellers = User.objects.all()
        makers = OfficialMakerName.objects.all()
        categories = EquipGroup.objects.all()
        seeder.add_entity(
            Product,
            number,
            {
                "seller": lambda x: random.choice(sellers),
                "maker": lambda x: random.choice(makers),
                "num_product": lambda x: random.randint(0, 100),
                "contact_person": lambda x: seeder.faker.name(),
                "contact_info": lambda x: seeder.faker.phone_number(),
                "category": lambda x: random.choice(categories),
            },
        )
        # 생성된 company의 pk번호를 dictionary형태로 return한다
        # {<class 'users.models.Company'>: [22, 23]}
        created_pk = seeder.execute()
        created_pk = flatten(list(created_pk.values()))

        # MtoM 필드 생성 방법
        for pk in created_pk:
            # 생성된 Company 객체를 선택한다
            product = Product.objects.get(pk=pk)
            # 선택된 Company 객체에 임의의 갯수의 사진을 입력한다
            for i in range(1, random.randint(2, 6)):
                Photo.objects.create(
                    product=product,
                    file=f"product_photos/{random.randint(1, 27)}.jpg",
                )
        self.stdout.write(self.style.SUCCESS(f"{number} product created!"))
