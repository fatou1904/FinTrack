from django.urls import path
from categories.views import CategorieListView, CategorieDetailView, CategorieCreateView

urlpatterns = [
    path('categories/', CategorieCreateView.as_view(), name='categorie-list'),
    path('categories/create/', CategorieListView.as_view(), name='categorie-list'),
    path('categories/<int:pk>/', CategorieDetailView.as_view(), name='categorie-detail'),
]
