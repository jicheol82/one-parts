from django.db import models

# from . import managers


class TimeStampedModel(models.Model):

    """Time Stamped Model"""

    name = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # objects = managers.CustomModelManager()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name
