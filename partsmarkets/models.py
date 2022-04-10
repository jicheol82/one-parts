from django.db import models
from django.core.validators import MinValueValidator
from core.models import TimeStampedModel
from users.models import User, EquipGroup
from virtualpools.models import OfficialMakerName

# Part Market 등록 상품
class Photo(TimeStampedModel):

    """Photo Model Definition"""

    file = models.ImageField(upload_to="product_photos")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)


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
    category = models.ForeignKey(EquipGroup, on_delete=models.SET_NULL, null=True)

    def seller_name(self):
        return self.seller.nickname

    seller_name.short_description = "Seller"

    def first_photo(self):
        (photo,) = self.photo_set.all()[:1]
        return photo.file.url

    def __str__(self):
        return f"'{self.maker}' / '{self.product_name}' / '{self.model_name}'"
