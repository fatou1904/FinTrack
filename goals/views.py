from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from goals.models import Objectif
from goals.serializer import GoalsSerializer

class ObjectifCreateList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        objectifs = Objectif.objects.filter(user=request.user)
        serializer = GoalsSerializer(objectifs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GoalsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
