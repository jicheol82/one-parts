from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import render, redirect, reverse
from django.db.models import Q
from django.contrib import messages
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


class VirtualPoolDetailView(OnlyForVerifiedMember, DetailView):
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

    def get_object(self, queryset=None):
        stockinfo = super().get_object(queryset=queryset)
        if stockinfo.owner.pk != self.request.user.pk:
            messages.error(self.request, "You're not allow to see this parts")
        return stockinfo


def VirtualPoolCreateView(request):
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


class VirutalPoolUpdateView(UpdateView):
    model = models.StockInfo
    fields = (
        "num_stock",
        "place",
        "is_new",
        "contact_person",
        "contact_info",
    )
    template_name = "virtualpools/update.html"
    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context[""]
    #     return super().get_context_data(**kwargs)


def VirtualPoolDeleteView(request, pk):
    user = request.user
    try:
        stockinfo = models.StockInfo.objects.get(pk=pk)
        if stockinfo.owner.pk != user.pk:
            messages.error(request, "Can't delete!")
        else:
            models.StockInfo.objects.filter(pk=pk).delete()
            messages.success(request, "Stock Deleted")
        return redirect("virtualpools:virtualpool")
    except models.StockInfo.DoesNotExist:
        return redirect("virtualpools:virtualpool")
