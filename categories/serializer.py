from rest_framework import serializers

from categories.models import Categorie

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'