from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel

# 회사 이름 집합 ex) (mhi, 미쯔비시중공업, mhps) -> MPW
class OfficialMakerName(TimeStampedModel):
    """Official Maker Name Model Definition"""

    name = models.CharField(_("official company name"), max_length=30, unique=True)


# 옛날 회사명
class OldMakerName(TimeStampedModel):
    """Old Maker Name Model Definition"""

    name = models.CharField(_("old manufacturer name"), max_length=30, unique=True)
    official_name = models.ForeignKey("OfficialMakerName", on_delete=models.CASCADE)


# Virtual Pool 등록 상품
class Stock(TimeStampedModel):
    """Stock Information Model Definition"""

    name = models.CharField(_("stock name"), max_length=30)
    maker = models.ForeignKey(
        "OfficialMakerName",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("manufacturer"),
    )
    model_name = models.CharField(_("model"), max_length=30)
    spec = models.CharField(_("specification"), max_length=30, blank=True)
    # 재고품 총 갯수
    def total_stock(self):
        stockinfo_objs = self.stockinfo_set.all()
        total = 0
        for i in stockinfo_objs:
            total += i.num_stock
        return total

    def owner_info(self):
        stockinfo_objs = self.stockinfo_set.all()
        owner_list = []
        for i in stockinfo_objs:
            owner_list.append(i.owner)
        return owner_list


# Virtual Pool 사용자의 등록 정보
class StockInfo(TimeStampedModel):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name=_("owner"),
    )
    my_stock = models.ForeignKey("Stock", on_delete=models.CASCADE)
    num_stock = models.IntegerField(
        _("num of stocks"), validators=[MinValueValidator(0)]
    )
    place = models.CharField(_("using place"), max_length=30)
    is_new = models.BooleanField(_("new part"))
    contact_person = models.CharField(_("person in charge"), max_length=20, blank=True)
    contact_info = models.CharField(_("contact information"), max_length=30, blank=True)
