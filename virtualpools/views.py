from urllib.request import HTTPRedirectHandler
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from core.mixins import OnlyForMember, OnlyForVerifiedMember
from . import models, forms


# 회사인증이 완료된 사람만 조회가능
# 로그인/리스트나 reservation을 배워야 할 듯
class VirtualPoolView(OnlyForVerifiedMember, ListView):
    model = models.StockInfo
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"

    def get_queryset(self):
        pk = self.request.user.pk
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search is not None:
            queryset = queryset.filter(
                Q(owner=pk),
                (
                    Q(my_stock__name__contains=search)
                    | Q(my_stock__maker__name__contains=search)
                    | Q(my_stock__model_name__contains=search)
                ),
            )
        else:
            queryset = queryset.filter(owner=pk)
        return queryset

    # 검색어 창에 검색어를 남기고, 검색결과에 대한 pagination을 위해 context를 추가
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search:
            context["input"] = search
        return context


@login_required(login_url="core:login")
def virtualpoolDetailView(request, pk):
    try:
        stockinfo = models.StockInfo.objects.get(pk=pk)
        if stockinfo.owner.pk != request.user.pk:
            messages.error(request, "You're not allow to see this parts")
            return redirect("virtualpools:virtualpool")
        else:
            return render(
                request, "virtualpools/stockinfo_detail.html", {"stockinfo": stockinfo}
            )
    except models.StockInfo.DoesNotExist:
        raise Http404()


@login_required(login_url="core:login")
def virtualPoolCreateView(request):
    if request.method == "POST":
        stock_form = forms.CreateStockForm(request.POST)
        stockinfo_form = forms.CreateStockInfoForm(request.POST)
        if stock_form.is_valid() and stockinfo_form.is_valid():
            stock_pk = stock_form.save()
            stockinfo = stockinfo_form.save(commit=False)
            stockinfo.owner = request.user
            stockinfo.my_stock = stock_pk
            stockinfo.save()
            return redirect("virtualpools:virtualpool")
        else:
            context = {
                "stock_form": stock_form,
                "stockinfo_form": stockinfo_form,
            }
    else:
        context = {
            "stock_form": forms.CreateStockForm(),
            "stockinfo_form": forms.CreateStockInfoForm(),
        }
    return render(request, "virtualpools/create.html", context)


class OnlyForOwner(UserPassesTestMixin):
    def test_func(self):
        pk = self.kwargs["pk"]
        user_pk = self.request.user.pk
        stockinfo = models.StockInfo.objects.get(pk=pk)
        if stockinfo.owner.pk != user_pk:
            return False
        else:
            return True

    def handle_no_permission(self):
        messages.error(self.request, "You're not allow to edit this part.")
        return redirect("virtualpools:virtualpool")


class VirutalPoolEditView(OnlyForOwner, UpdateView):
    model = models.StockInfo
    fields = (
        "num_stock",
        "place",
        "is_new",
        "contact_person",
        "contact_info",
    )
    template_name = "virtualpools/edit.html"


def virtualPoolDeleteView(request, pk):
    user = request.user
    try:
        stockinfo = models.StockInfo.objects.get(pk=pk)
        if stockinfo.owner.pk != user.pk:
            messages.error(request, "Can't delete!")
        else:
            stockinfo.delete()
            messages.success(request, "Stock Deleted")
        return redirect("virtualpools:virtualpool")
    except models.StockInfo.DoesNotExist:
        return redirect("virtualpools:virtualpool")
