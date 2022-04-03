from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel

# 설비관련 모델 생성하기
class AbstractItem(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class EquipGroup(AbstractItem):
    class Meta:
        verbose_name_plural = "Equipment Groups"


class Equipment(AbstractItem):
    equipment_group = models.ForeignKey(
        EquipGroup, on_delete=models.SET_NULL, null=True
    )


# 회사관련 모델 생성하기
class Domain(AbstractItem):
    pass


class Branch(AbstractItem):
    pass


class Company(AbstractItem):
    domains = models.ManyToManyField(Domain, blank=True)
    branches = models.ManyToManyField(Branch, blank=True)


# 사용자 모델 생성하기
class User(AbstractUser):
    # username은 15.1에서 form.py에서 save()를 overide 하여 email로 저장한다
    profile_img = models.ImageField(upload_to="profile_img", blank=True)
    nickname = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20, blank=True)
    company_email = models.EmailField(blank=True)
    my_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    my_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    interesting_equips = models.ManyToManyField(Equipment, blank=True)

    def save_domain(self):
        email = self.company_email
        domain = "@" + email.split("@")[1]
        try:
            Domain.objects.get(name=domain)
            return f"{domain} is alreay exist"
        except Domain.DoesNotExist:
            Domain.objects.create(name=domain)
            return f"{domain} is registered!"

    def save_branch(self):
        branch = self.my_branch
        try:
            Branch.objects.get(name=branch)
            return f"{branch} is alreay exist"
        except Branch.DoesNotExist:
            Branch.objects.create(name=branch)
            return f"{branch} is registered!"

    def save_company(self):
        company = self.my_company
        try:
            Company.objects.get(name=company)
            return f"{company} is alreay exist"
        except Company.DoesNotExist:
            Company.objects.create(name=company)
            return f"{company} is registered!"
