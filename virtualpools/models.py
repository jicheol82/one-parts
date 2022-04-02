from django.db import models
from django.core.validators import MinValueValidator
from core.models import TimeStampedModel
from users.models import User


class AbstractMaker(TimeStampedModel):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# 회사 이름 집합 ex) (mhi, 미쯔비시중공업, mhps) -> MPW
class OtherMakerName(AbstractMaker):
    """SimilarName Model Definition"""

    pass


class OfficialMakerName(AbstractMaker):
    """Maker Model Definition"""

    other_names = models.ManyToManyField(OtherMakerName, blank=True)


# Virtual Pool 등록 상품
class Stock(TimeStampedModel):
    stock_name = models.CharField(max_length=140)
    maker = models.ForeignKey(OfficialMakerName, on_delete=models.SET_NULL, null=True)
    model_name = models.CharField(max_length=140)
    spec = models.CharField(max_length=180, blank=True)
    # 재고품 총 갯수
    def total_stock(self):
        return self.stockinfo_set.count()

    def __str__(self):
        return f"'{self.maker}' / '{self.stock_name}' / '{self.model_name}'"


# Virtual Pool 사용자의 등록 정보
class StockInfo(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    my_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    num_stock = models.IntegerField(validators=[MinValueValidator(1)])
    place = models.CharField(max_length=80)
    new_part = models.BooleanField()
    contact_person = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=100, blank=True)
    # __str__은 string을 return해야 한다
    def __str__(self):
        return str(self.my_stock)
