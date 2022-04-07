from django.views.generic import ListView, DetailView
from django.db.models import Q
from . import models

# 내가 등록한 부품만 보이게 하는 것은 수업을 더 듣고 작성한다
# 로그인/리스트나 reservation을 배워야 할 듯
class VirtualPoolView(ListView):
    model = models.StockInfo
    paginate_by = 10
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


class DetailView(DetailView):
    model = models.StockInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_stock"] = models.Stock.total_stock(self.object.my_stock)
        return context
