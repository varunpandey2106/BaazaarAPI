from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User= get_user_model()

class TimeStampedModel(models.Model):
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Notification(TimeStampedModel):

    MARKED_READ = "r"
    MARKED_UNREAD = "u"

    CHOICES = ((MARKED_READ, "read"), (MARKED_UNREAD, "unread"))

    user = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    status = models.CharField(choices=CHOICES, default=MARKED_UNREAD, max_length=1)