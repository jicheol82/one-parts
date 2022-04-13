from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.urls import reverse_lazy
from core.mixins import OnlyForMember
from . import models

# 회사인증이 완료된 사람만 조회가능
# 로그인/리스트나 reservation을 배워야 할 듯
class VirtualPoolView(OnlyForMember, ListView):
    model = models.StockInfo
    paginate_by = 25
    paginate_orphans = 5
    ordering = "created"

    def get_queryset(self):
        pk = self.request.user.pk
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search is not None:
            queryset = queryset.filter(
                Q(pk=pk),
                (
                    Q(my_stock__stock_name__contains=search)
                    | Q(my_stock__maker__name__contains=search)
                    | Q(my_stock__model_name__contains=search)
                ),
            )
        else:
            queryset = queryset.filter(pk=pk)
        return queryset

    # 검색어 창에 검색어를 남기고, 검색결과에 대한 pagination을 위해 context를 추가
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search:
            context["input"] = search
        return context


# 회사인증이 완료된 사람만 조회가능
# 본인의 재고가 아닌 것은 안보이게 하기-어떻게?
class VirtualPoolDetailView(OnlyForMember, DetailView):
    model = models.StockInfo
    fields = (
        "my_stock.maker",
        "my_stock.stock_name",
        "num_stock",
        "my_stock.total_stock",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_stock"] = models.Stock.total_stock(self.object.my_stock)
        context["owner_info"] = models.Stock.owner_info(self.object.my_stock)
        return context
