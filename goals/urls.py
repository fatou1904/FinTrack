from django.urls import path

from goals.views import ObjectifCreateList

urlpatterns = [
    path('objectif/', ObjectifCreateList.as_view(), name='objectif' )
]
