from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel

# Part Market 등록 상품
class Photo(TimeStampedModel):
    """Photo Model Definition"""

    file = models.ImageField(upload_to="product_photos")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)


class Product(TimeStampedModel):
    """Product Model Definition"""

    name = models.CharField(max_length=30)
    seller = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name=_("seller")
    )
    maker = models.ForeignKey(
        "virtualpools.OfficialMakerName",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("manufacturer"),
    )
    model_name = models.CharField(_("model"), max_length=30)
    spec = models.CharField(_("specification"), max_length=30, blank=True)
    description = models.TextField(_("description"), blank=True)
    num_product = models.IntegerField(
        _("number of products"), validators=[MinValueValidator(0)]
    )
    is_new = models.BooleanField(_("new part"), default=True)
    contact_person = models.CharField(_("person in charge"), max_length=20, blank=True)
    contact_info = models.CharField(_("contact information"), max_length=30, blank=True)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    category = models.ForeignKey(
        "users.EquipGroup",
        on_delete=models.SET_NULL,
        null=True,
    )
    on_sale = models.BooleanField(_("on sale"), blank=True, default=False)

    def first_photo(self):
        (photo,) = self.photo_set.all()[:1]
        return photo.file.url
