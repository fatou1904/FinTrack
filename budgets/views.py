from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Budget
from .serializer import BudgetSerializer
from rest_framework.permissions import IsAuthenticated

class BudgetListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BudgetDetailView(APIView):
    def get_object(self, pk):
        try:
            return Budget.objects.get(pk=pk)
        except Budget.DoesNotExist:
            raise NotFound(detail="Budget not found", code=404)

    def get(self, request, pk):
        budget = self.get_object(pk)
        serializer = BudgetSerializer(budget)
        return Response(serializer.data)

    def put(self, request, pk):
        budget = self.get_object(pk)
        serializer = BudgetSerializer(budget, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        budget = self.get_object(pk)
        budget.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
