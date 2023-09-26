from rest_framework import serializers
from fcm_django.models import FCMDevice #sending push notifications
from .models import Notification

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = [
            "name",
            "active",
            "user",
            "device_id",
            "registration_id",
            "type",
            "date_created",
        ]

