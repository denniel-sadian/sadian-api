from django.conf import settings
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Day
from .serielizers import DaySerializer


class DayViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = ()
    serializer_class = DaySerializer
    queryset = Day.objects.all()


@api_view(['GET'])
def profile_picture(request):
    link = settings.PROFILE_PICTURE
    return Response(data=link, status=status.HTTP_200_OK)

