import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel


class EquipGroup(TimeStampedModel):
    name = models.CharField(_("equipment Group"), max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name


class Equipment(TimeStampedModel):
    name = models.CharField(_("equipment"), max_length=20, unique=True)
    group = models.ForeignKey("EquipGroup", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name


# 회사관련 모델 생성하기
class Branch(TimeStampedModel):
    name = models.CharField(_("branch"), max_length=20)

    class Meta:
        verbose_name_plural = _("branches")

    def __str__(self) -> str:
        return self.name


class Company(TimeStampedModel):
    name = models.CharField(_("company"), max_length=20)
    branches = models.ManyToManyField("users.Branch", blank=True)

    class Meta:
        verbose_name_plural = _("companies")

    def __str__(self) -> str:
        return self.name


class Domain(TimeStampedModel):
    name = models.CharField(_("domain"), max_length=20, unique=True)
    company = models.ForeignKey("users.Company", on_delete=models.CASCADE)


# 사용자 모델 생성하기
class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, unique=True)
    profile_img = models.ImageField(_("picture"), upload_to="profile_img", blank=True)
    company = models.ForeignKey("Company", on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey("Branch", on_delete=models.SET_NULL, null=True)
    my_equips = models.ManyToManyField(
        "Equipment", blank=True, verbose_name=_("equipment")
    )
    is_verified = models.BooleanField(_("verification"), default=False)
    token = models.CharField(max_length=20, blank=True)

    def save_domain(self):
        domain = self.email.split("@")[1]
        try:
            Domain.objects.get(name=domain)
            return f"{domain} is alreay exist"
        except Domain.DoesNotExist:
            Domain.objects.create(name=domain)
            return f"{domain} is registered!"

    def save_branch(self):
        branch = self.branch
        try:
            Branch.objects.get(name=branch)
            return f"{branch} is alreay exist"
        except Branch.DoesNotExist:
            Branch.objects.create(name=branch)
            return f"{branch} is registered!"

    def save_company(self):
        company = self.company
        try:
            Company.objects.get(name=company)
            return f"{company} is alreay exist"
        except Company.DoesNotExist:
            Company.objects.create(name=company)
            return f"{company} is registered!"

    def verify_email(self):
        key = uuid.uuid4().hex[:8]
        self.token = key
        print("key :", key)
        html_message = render_to_string("emails/verify_user.html", {"secret": key})
        try:
            send_mail(
                _("Please Complete Email Verification"),
                html_message,
                from_email=settings.EMAIL_FROM,
                recipient_list=[self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        except Exception as e:
            print("Exception happend : ", e)
            pass

    def get_absolute_url(self):
        return reverse("users:account")
