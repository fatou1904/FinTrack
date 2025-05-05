from django.urls import path

from notification.views import NotificationList, NotificationMarkAsRead

urlpatterns = [
    path('notification/', NotificationList.as_view(), name='notification' ),
     path('notifications/<int:pk>/mark-read/', NotificationMarkAsRead.as_view(), name='notification-mark-read'),
]
