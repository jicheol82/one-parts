import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from partsmarket.models import Product, Photo
from users.models import User, EquipGroup
from virtualpools.models import OfficialMakerName


class Command(BaseCommand):

    help = "This command creates products"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many products you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        # 생성되어 있는 모든 User, OfficialMakerName, EquipGroup 객체를 가져온다-좋은 방법은 아님
        sellers = User.objects.all()
        makers = OfficialMakerName.objects.all()
        categories = EquipGroup.objects.all()
        seeder.add_entity(
            Product,
            number,
            {
                # lambda가 없이 실행하면 add_entity가 생성될때 입력값을 먼저 저장하고 횟수만큼 반복하지 않는 것같다
                # lambda가 있어야지 매번 새로운 값이 호출될 수 있다
                # MtoM 필드는 여기서 생성 불가
                "seller": lambda x: random.choice(sellers),
                "maker": lambda x: random.choice(makers),
                "contact_person": lambda x: seeder.faker.name(),
                "contact_number": lambda x: seeder.faker.phone_number(),
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
                    file=f"product_photos/{random.randint(1, 31)}.webp",
                )
        self.stdout.write(self.style.SUCCESS(f"{number} product created!"))
