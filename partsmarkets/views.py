from django.views.generic import ListView, DetailView
from django.db.models import Q
from . import models


class PartsMarketView(ListView):
    model = models.Product
    paginate_by = 16
    paginate_orphans = 12
    ordring = "created"
    # 다중쿼리를 이용함으로써 검색필드를 제거함
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search is not None:
            queryset = queryset.filter(
                Q(product_name__contains=search)
                | Q(maker__name__contains=search)
                | Q(model_name__contains=search)
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
    model = models.Product
