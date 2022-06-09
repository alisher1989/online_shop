from rest_framework import viewsets
from webapp.models import Advantages, About_us
from webapp.serializers import AdvantagesSerializer, About_usSerializer


class AdvantagesViewSet(viewsets.ModelViewSet):
    """Список преимуществ"""
    queryset = Advantages.objects.all()
    serializer_class = AdvantagesSerializer


class About_usViewSet(viewsets.ModelViewSet):
    """Инфо о нас"""
    queryset = About_us.objects.all()
    serializer_class = About_usSerializer
