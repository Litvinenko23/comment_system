from django.db import models


class Comment(models.Model):
    message = models.TextField()
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    def __str__(self):
        return self.message
