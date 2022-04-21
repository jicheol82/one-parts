from django.shortcuts import render
from django.views.generic import ListView, View
from django.db.models import Q
from core.mixins import OnlyForVerifiedMember
from .models import *

# Create your views here.
class FeedView(ListView):
    model = Feed
    paginate_by = 20
    paginate_orphans = 12
    ordring = "created"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search is not None:
            queryset = queryset.filter(
                Q(writer__contains=search) | Q(content__contains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search:
            context["input"] = search
        return context


class ReplyView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        obj_list = Reply.objects.filter(original_feed=pk)
        return render(request, "communities/reply_list.html", {"obj_list": obj_list})
