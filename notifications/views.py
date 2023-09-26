from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework import permissions, status
from .serializers import NotificationMiniSerializer
from .models import Notification
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

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
    

    

