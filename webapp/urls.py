from django.urls import path
from webapp.views import AdvantagesViewSet

urlpatterns = [
    path('', AdvantagesViewSet.as_view({'get': 'list'})),
]
