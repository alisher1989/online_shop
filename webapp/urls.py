from django.urls import path

from webapp.views import AdvantagesViewSet, About_usViewSet, HelpViewSet, ApiView, HelpImageViewSet, NewsViewSet, \
    CollectionViewSet, ItemViewSet, SimilarItemViewSet

urlpatterns = [
    path('advantages/', AdvantagesViewSet.as_view({'get': 'list'})),
    path('about/', About_usViewSet.as_view({'get': 'list'})),
    path('news/', NewsViewSet.as_view({'get': 'list'})),
    path('collection/', CollectionViewSet.as_view({'get': 'list'})),
    path('help/', HelpViewSet.as_view({'post': 'create'})),
    path('imagehelp/', HelpImageViewSet.as_view({'post': 'create'})),
    path('help/<int:pk>/', HelpViewSet.as_view({'put': 'update', 'get': 'retrieve'})),
    path('answers/', ApiView.as_view()),
    path('item/<int:pk>/', ItemViewSet.as_view({'get': 'retrieve'})),
    path('similar/<int:pk>/', SimilarItemViewSet.as_view({'get': 'retrieve'})),
]
