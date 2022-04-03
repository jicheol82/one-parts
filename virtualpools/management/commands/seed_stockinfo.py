import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User
from virtualpools.models import StockInfo, Stock

TITLE = "stockinfos"


class Command(BaseCommand):

    help = f"This command creates {TITLE}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help=f"How many {TITLE} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        # 생성되어 있는 모든 User, Stock 객체를 가져온다-좋은 방법은 아님
        owner = User.objects.all()
        my_stock = Stock.objects.all()
        seeder.add_entity(
            StockInfo,
            number,
            {
                # lambda가 없이 실행하면 add_entity가 생성될때 입력값을 먼저 저장하고 횟수만큼 반복하지 않는 것같다
                # lambda가 있어야지 매번 새로운 값이 호출될 수 있다
                # MtoM 필드는 여기서 생성 불가
                "owner": lambda x: random.choice(owner),
                "my_stock": lambda x: random.choice(my_stock),
                "num_stock": lambda x: random.randint(1, 100),
                "contact_person": lambda x: seeder.faker.name(),
                "contact_number": lambda x: seeder.faker.phone_number(),
            },
        )
        # 생성된 company의 pk번호를 dictionary형태로 return한다
        # {<class 'users.models.Company'>: [22, 23]}
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} {TITLE} created!"))
