from django.urls import path
from .views import NotificationViewSet

urlpatterns = [
    path('', NotificationViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='notification-list'),

    path('<int:pk>/', NotificationViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    }), name='notification-detail'),

    path('<int:pk>/marquer-lue/', NotificationViewSet.as_view({
        'post': 'marquer_comme_lue'
    }), name='notification-marquer-lue'),

    path('marquer-tout-lu/', NotificationViewSet.as_view({
        'post': 'tout_marquer_comme_lu'
    }), name='notifications-marquer-tout-lu'),

    path('non-lues/', NotificationViewSet.as_view({
        'get': 'non_lues'
    }), name='notifications-non-lues'),
]
