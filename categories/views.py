# categories/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Categorie
from .serializer import CategoriesSerializer

class CategorieCreateView(APIView):
    def post(self, request):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategorieListView(APIView):
    def get(self, request):
        categories = Categorie.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

class CategorieDetailView(APIView):
    def get_object(self, pk):
        try:
            return Categorie.objects.get(pk=pk)
        except Categorie.DoesNotExist:
            raise NotFound(detail="Categorie not found", code=404)

    def get(self, request, pk):
        categorie = self.get_object(pk)
        serializer = CategoriesSerializer(categorie)
        return Response(serializer.data)
