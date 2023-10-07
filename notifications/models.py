from django.db import models
from django.contrib.auth import get_user_model
from twilio.rest import Client

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

class TwilioNotif(models.Model):
    test_result = models.PositiveIntegerField()

    #string representation
    def __str__(self):
        return str(self.test_result)
    
    def save(self, *args, **kwargs):
        #if test_result is less than 80 execute this
        if self.test_result < 80:
            #twilio code
            account_sid = "AC4a51dde40cbbe0cb0d4d648f7372f003"
            auth_token = "8f6c1b1fb0fa2db1512007e069fed879"
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                                        body=f'Hi, your test result is {self.test_result}. Great job',
                                        from_='+12563443401',
                                        to='+918355921551' 
                                    )

            print(message.sid)
        return super().save(*args, **kwargs)