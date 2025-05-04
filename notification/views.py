from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(utilisateur=self.request.user)

    @action(detail=True, methods=['post'])
    def marquer_comme_lue(self, request, pk=None):
        notification = self.get_object()
        notification.est_vue = True
        notification.save()
        return Response({'status': 'Notification marquée comme lue'})

    @action(detail=False, methods=['post'])
    def tout_marquer_comme_lu(self, request):
        self.get_queryset().update(est_vue=True)
        return Response({'status': 'Toutes les notifications ont été marquées comme lues'})

    @action(detail=False, methods=['get'])
    def non_lues(self, request):
        notifications = self.get_queryset().filter(est_vue=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
