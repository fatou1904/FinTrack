from django.urls import path
from rest_framework.routers import DefaultRouter
from depense.views import DepenseViewSet, BudgetViewSet

router = DefaultRouter()
router.register(r'depenses', DepenseViewSet, basename='depense')
router.register(r'budgets', BudgetViewSet, basename='budget')

urlpatterns = router.urls 
