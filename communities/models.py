from django.db import models
from core.models import TimeStampedModel
from users.models import User


class Feed(TimeStampedModel):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    attach = models.FileField("Attachment", upload_to="uploads/", blank=True)

    def count_reply(self):
        return self.reply_set.count()

    count_reply.short_description = "#Reply"

    def __str__(self):
        return self.content[:100]


class Reply(TimeStampedModel):
    original_feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    # 향후, 탈퇴하더라도 댓글은 지워지지 않고, 최종 닉네임이 남도록 한다
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.writer}-{self.content[:100]}"
