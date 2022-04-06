from django.views.generic import ListView
from django.db.models import Q
from . import models as vp_models

# 내가 등록한 부품만 보이게 하는 것은 수업을 더 듣고 작성한다
# 로그인/리스트나 reservation을 배워야 할 듯
class VirtualPoolView(ListView):
    model = vp_models.StockInfo
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"

    def get_queryset(self):
        queryset = super().get_queryset()
        range = self.request.GET.get("range")
        search_kwarg = self.request.GET.get("search_kwarg")
        if search_kwarg is not None:
            if search_kwarg is not None:
                if range == "stock_name":
                    queryset = queryset.filter(
                        my_stock__stock_name__contains=search_kwarg
                    )
                elif range == "maker":
                    queryset = queryset.filter(
                        my_stock__maker__name__contains=search_kwarg
                    )
                elif range == "model_name":
                    queryset = queryset.filter(
                        my_stock__model_name__contains=search_kwarg
                    )
                else:
                    # 무언가 처리 해줘야 할 듯...
                    print("dont touch keys")
        return queryset


# 검색결과에 대한 pagination
