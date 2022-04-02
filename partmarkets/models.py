from operator import truediv
from django.db import models
from django.core.validators import MinValueValidator
from core.models import TimeStampedModel
from users.models import User, EuipGroup
from virtualpools.models import OfficialMakerName

# Part Market 등록 상품
class Product(TimeStampedModel):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=140)
    maker = models.ForeignKey(OfficialMakerName, on_delete=models.SET_NULL, null=True)
    model_name = models.CharField(max_length=140)
    spec = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    num_product = models.IntegerField(validators=[MinValueValidator(0)])
    new_part = models.BooleanField()
    contact_person = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    category = models.ForeignKey(EuipGroup, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"'{self.maker}' / '{self.product_name}' / '{self.model_name}'"
