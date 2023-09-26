from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import NotificationMiniSerializer, FCMDeviceSerializer
from .models import Notification
from rest_framework.exceptions import PermissionDenied, NotAcceptable
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from fcm_django.models import FCMDevice

# Create your views here.
class NotificationListView(ListAPIView):  #get list of all notifs of user
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationMiniSerializer

    def get_queryset(self): 
        user = self.request.user #currently authenticated user
        queryset = Notification.objects.filter(
            user=user, status=Notification.MARKED_UNREAD
        ).order_by("-created")
        return queryset
    

class NotificationAPIView(RetrieveDestroyAPIView): #retrieve and delete a single notif
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationMiniSerializer
    queryset = Notification.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        notification = self.get_object()
        if notification.user != user: #authenticated users only
            raise PermissionDenied("this notification does not belong to you")
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        notification = self.get_object()
        if notification.user != user:
            raise PermissionDenied(
                "this notification not belong to you,you can't delete this notification"
            )
        notification.delete()
        return Response(
            {"detail": _("this notification is deleted successfuly.")},
            status=status.HTTP_204_NO_CONTENT,
        )

class MarkedAllAsReadNotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request): #mark all unread as read
        user = request.user
        notifications = Notification.objects.filter(
            user=user, status=Notification.MARKED_UNREAD
        )
        for notification in notifications:
            if notification.user != user:
                raise PermissionDenied("this notifications don't belong to you.")
            notification.status = Notification.MARKED_READ
            notification.save()
        return Response("No new notifications.", status=status.HTTP_200_OK)

    
class CreateDeviceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(
        self, request,
    ):
        user = request.user
        registration_id = request.data.get("registration_id", None)
        type = request.data.get("type", None)
        device = FCMDevice.objects.filter(registration_id=registration_id, type=type)
        if device.count() > 0:
            raise NotAcceptable("This Device is Founded.")
        serializer = FCMDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

