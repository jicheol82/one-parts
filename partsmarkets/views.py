from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
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
        else:
            queryset = queryset.filter(on_sale=True)
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


class OnlyForOwner(UserPassesTestMixin):
    def test_func(self):
        pk = self.kwargs["pk"]
        user_pk = self.request.user.pk
        product = models.Product.objects.get(pk=pk)
        if product.seller.pk != user_pk:
            return False
        else:
            return True

    def handle_no_permission(self):
        messages.error(self.request, "You're not allow to edit this product.")
        return redirect("partsmarkets:partsmarket")


class PartsMarketEditView(OnlyForOwner, UpdateView):
    model = models.Product
    fields = (
        "description",
        "num_product",
        "contact_person",
        "contact_info",
        "price",
        "on_sale",
    )
    template_name = "partsmarkets/edit.html"


def partsMarketDeleteView(request, pk):
    user = request.user
    try:
        product = models.Product.objects.get(pk=pk)
        if product.seller.pk != user.pk:
            messages.error(request, "Can't delete!")
        else:
            models.Product.objects.filter(pk=pk).delete()
            messages.success(request, "Product Deleted")
        return redirect("partsmarkets:partsmarket")
    except models.Product.DoesNotExist:
        return redirect("partsmarkets:partsmarket")
