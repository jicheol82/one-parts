import json
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from psycopg2 import IntegrityError
from core.mixins import OnlyForMember
from .models import *
from .forms import FeedWriteForm

# Create your views here.
class FeedListView(ListView):
    model = Feed
    paginate_by = 20
    paginate_orphans = 12
    ordering = ["-created"]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search is not None:
            queryset = queryset.filter(
                Q(writer__username__contains=search) | Q(content__contains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        if search:
            context["input"] = search
        return context


class FeedDetailView(OnlyForMember, DetailView):
    model = Feed
    fields = (
        "writer",
        "content",
        "created",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        replies = Reply.objects.filter(original_feed=pk)
        context["replies"] = replies
        return context


def feed_write(request):
    context = {}
    if request.method == "GET":
        write_form = FeedWriteForm()
        context["form"] = write_form
        return render(request, "communities/feed_create.html", context)
    elif request.method == "POST":
        write_form = FeedWriteForm(request.POST)
        return redirect("communities:feed")


class FeedWriteView_S(FormView):
    form_class = FeedWriteForm
    template_name = "communities/feed_create.html"
    success_url = reverse_lazy("communities:feed_detail")

    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)

    def get_success_url(self) -> str:
        print(self.pk)
        return reverse("communities:feed_detail", kwargs={"pk": self.pk})


class FeedCreateView(OnlyForMember, CreateView):
    model = Feed
    fields = (
        "writer",
        "content",
        "attach",
    )
    template_name = "communities/feed_create.html"


class FeedUpdateView(UpdateView):
    model = Feed
    fields = (
        "content",
        "attach",
    )
    template_name = "communities/feed_create.html"


def feedDelete(request, pk):
    user = request.user
    try:
        feed = Feed.objects.get(pk=pk)
        if feed.writer.pk != user.pk:
            messages.success(request, "Can't Deleted")
        else:
            result = feed.delete()
            print(result)
            messages.success(request, "Feed Deleted")
    except Feed.DoesNotExist:
        messages.success(request, "It's been deleted already")
    finally:
        return redirect("communities:feed")


@csrf_exempt
def replyCreateView(request, pk):
    if request.method == "POST":
        bodydata = request.body.decode("utf-8")
        bodyjson = json.loads(bodydata)
        text = bodyjson["reply"]
        user = request.user
        original_feed = Feed.objects.get(pk=pk)
        context = {}
        try:
            new_reply = Reply.objects.create(
                original_feed=original_feed, writer=user, content=text
            )
            context["pk"] = new_reply.pk
            context["writer"] = new_reply.writer.username
            context["content"] = new_reply.content
            return JsonResponse(context, content_type="application/json")
        except IntegrityError:
            return


def replyDeleteView(request, pk, r_pk):
    user = request.user
    context = {}
    try:
        reply = Reply.objects.get(pk=r_pk)
        if reply.writer.pk != user.pk:
            context["result"] = "Can't delete"

        else:
            reply.delete()
            context["result"] = "Deleted"
    except Feed.DoesNotExist:
        context["result"] = "There is no target reply"
    finally:
        return JsonResponse(context, content_type="application/json")
