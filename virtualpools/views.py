from django.views.generic import ListView
from django.shortcuts import render
from . import models

# 내가 등록한 부품만 보이게 하는 것은 수업을 더 듣고 작성한다
# 로그인/리스트나 reservation을 배워야 할 듯
class VirtualPoolView(ListView):
    model = models.StockInfo
    paginate_by = 10
    paginate_orphans = 5
    ordring = "created"
