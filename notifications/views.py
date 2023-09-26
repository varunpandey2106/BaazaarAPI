from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import permissions, status
from .serializers import NotificationMiniSerializer
from .models import Notification

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
    
    
    

