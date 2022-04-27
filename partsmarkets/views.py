from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.urls import reverse_lazy
from core.mixins import OnlyForVerifiedMember
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
                Q(name__contains=search)
                | Q(maker__name__contains=search)
                | Q(model_name__contains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search:
            context["input"] = search
        return context


class PartsMarketMyListView(ListView):
    model = models.Product
    paginate_by = 16
    paginate_orphans = 12
    ordring = "created"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(seller__pk=self.request.user.pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search:
            context["input"] = search
        return context


# 회사인증이 완료된 사람만 조회가능
class DetailView(OnlyForVerifiedMember, DetailView):
    model = models.Product

    login_url = reverse_lazy("core:login")
