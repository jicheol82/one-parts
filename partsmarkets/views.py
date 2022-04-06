from django.views.generic import ListView
from . import models


class PartsMarketView(ListView):
    model = models.Product
    paginate_by = 10
    paginate_orphans = 5
    ordring = "created"
