from django.urls import path
from .views import ObjectifViewSet

urlpatterns = [
    path('', ObjectifViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='objectif-list'),

    path('<int:pk>/', ObjectifViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='objectif-detail'),

    path('<int:pk>/contributions/', ObjectifViewSet.as_view({
        'get': 'list_contributions',
        'post': 'ajouter_contribution'
    }), name='objectif-contributions'),

    path('stats/', ObjectifViewSet.as_view({
        'get': 'get_stats'
    }), name='objectif-stats'),

    path('completed/', ObjectifViewSet.as_view({
        'get': 'objectifs_completes'
    }), name='objectif-completed'),
]
