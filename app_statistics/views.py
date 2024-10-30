# app_statistics/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .app_operations_statistics import StatisticsOperations

class StatisticsDashboardView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        stats = StatisticsOperations.calculate_user_statistics(request.user)
        return Response({'statistics': stats}, status=200)
