from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True, 
        editable=False,
        help_text="The datetime this object was created"
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text="The datetime this object was last updated"
    )

    class Meta:
        abstract = True