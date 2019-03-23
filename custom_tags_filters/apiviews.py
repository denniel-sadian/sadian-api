from rest_framework import viewsets

from .models import Day
from .serielizers import DaySerializer


class DayViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = ()
    serializer_class = DaySerializer
    queryset = Day.objects.all()
