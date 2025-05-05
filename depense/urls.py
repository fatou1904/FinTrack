from django.urls import path

from depense.views import DepenseList

urlpatterns = [
    path('depense/', DepenseList.as_view(), name='depense' )
]
