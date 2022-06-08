from rest_framework import viewsets
from webapp.models import Advantages
from webapp.serializers import AdvantagesSerializer


class AdvantagesViewSet(viewsets.ModelViewSet):
    queryset = Advantages.objects.all()
    serializer_class = AdvantagesSerializer

