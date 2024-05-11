from django.shortcuts import render
from rest_framework import viewsets
from ..models import Statistics
from ..serializers import StatisticsSerializer

class StatisticsViewSet(viewsets.ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer