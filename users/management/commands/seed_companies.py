import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users.models import Company, Domain, Branch


class Command(BaseCommand):

    help = "This command creates amenities"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        # 생성되어 있는 모든 Domain, Branch 객체를 가져온다-좋은 방법은 아님
        domains = Domain.objects.all()
        branches = Branch.objects.all()
        seeder.add_entity(
            Company,
            number,
            {
                # lambda가 없이 실행하면 add_entity가 생성될때 입력값을 먼저 저장하고 횟수만큼 반복하지 않는 것같다
                # lambda가 있어야지 매번 새로운 값이 호출될 수 있다
                # MtoM 필드는 여기서 생성 불가
                "name": lambda x: seeder.faker.company(),
            },
        )
        # 생성된 company의 pk번호를 dictionary형태로 return한다
        # {<class 'users.models.Company'>: [22, 23]}
        created_pk = seeder.execute()
        created_pk = flatten(list(created_pk.values()))

        # MtoM 필드 생성 방법
        for pk in created_pk:
            # 생성된 Company 객체를 선택한다
            company = Company.objects.get(pk=pk)
            # 생성된 Domain 객체를 임의로 선택한다
            random_items = random.sample(list(domains), random.randint(1, len(domains)))
            # 선택된 Domain 객체를 선택된 pk의 Company 객체에 추가한다
            company.domains.add(*random_items)
            # 생성된 Branch 객체를 임의로 선택한다
            random_items = random.sample(
                list(branches), random.randint(1, len(branches))
            )
            # 선택된 Branch 객체를 선택된 pk의 Company 객체에 추가한다
            company.branches.add(*random_items)
        self.stdout.write(self.style.SUCCESS(f"{number} companies created!"))
