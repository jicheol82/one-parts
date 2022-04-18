from django.db import models
from core.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

DEFAULT_PK = 1


class Feed(TimeStampedModel):
    """Feed Model Defenition"""

    writer = models.ForeignKey(
        "users.User",
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_PK,
        verbose_name=_("writer"),
    )
    content = models.TextField(_("content"))
    attach = models.FileField(
        _("attachment"),
        upload_to="uploads/",
        blank=True,
    )

    def count_reply(self):
        return self.reply_set.count()

    count_reply.short_description = _("#Reply")

    def __str__(self):
        return f"{self.writer}-{self.content[:40]}"


class Reply(TimeStampedModel):
    """Reply Model Defenition"""

    original_feed = models.ForeignKey("Feed", on_delete=models.CASCADE)
    # 향후, 탈퇴하더라도 댓글은 지워지지 않고, 최종 닉네임이 남도록 한다
    writer = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, verbose_name=_("writer")
    )
    content = models.TextField(_("content"))

    def __str__(self):
        return f"{self.writer}-{self.content[:40]}"
