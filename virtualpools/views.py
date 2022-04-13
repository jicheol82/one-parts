from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.urls import reverse_lazy
from core.mixins import OnlyForMember
from . import models

# 내가 등록한 부품만 보이게 하는 것은 수업을 더 듣고 작성한다
# 로그인/리스트나 reservation을 배워야 할 듯
class VirtualPoolView(OnlyForMember, ListView):
    model = models.StockInfo
    paginate_by = 25
    paginate_orphans = 5
    ordering = "created"

    # 다중쿼리를 이용함으로써 검색필드를 제거함
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search is not None:
            queryset = queryset.filter(
                Q(my_stock__stock_name__contains=search)
                | Q(my_stock__maker__name__contains=search)
                | Q(my_stock__model_name__contains=search)
            )
        return queryset

    # 검색어 창에 검색어를 남기고, 검색결과에 대한 pagination을 위해 context를 추가
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search:
            context["input"] = search
        return context


class VirtualPoolDetailView(OnlyForMember, DetailView):
    model = models.StockInfo
    fields = (
        "my_stock.maker",
        "my_stock.stock_name",
        "num_stock",
        "my_stock.total_stock",
    )
    labels = ({"num_stock": "test"},)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["total_stock"] = models.Stock.total_stock(self.object.my_stock)
    #     return context
