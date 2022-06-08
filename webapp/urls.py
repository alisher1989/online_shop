from django.urls import path
from webapp.views import AdvantagesViewSet, About_usViewSet

urlpatterns = [
    path('', AdvantagesViewSet.as_view({'get': 'list'})),
    path('about/', About_usViewSet.as_view({'get': 'list'})),
]
