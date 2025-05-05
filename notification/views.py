from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from notification.models import Notification
from notification.serializer import NotificationSerializer

class NotificationList(generics.ListAPIView):
    queryset = Notification.objects.filter(est_vue=False)
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, est_vue=False)

class NotificationMarkAsRead(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        notification_id = self.kwargs.get('pk')
        return Notification.objects.get(id=notification_id, user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.est_vue = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)