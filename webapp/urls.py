from django.urls import path

from webapp.views import AdvantagesViewSet, About_usViewSet, HelpViewSet, ApiView, HelpImageViewSet, NewsViewSet, \
    CollectionViewSet, ItemViewSet, SimilarItemViewSet, CollectionDetailViewSet, CollectionDetailViewSet2, \
    NewProductDetailViewSet, FavoriteProductDetailViewSet

urlpatterns = [
    path('advantages/', AdvantagesViewSet.as_view({'get': 'list'})),
    path('about/', About_usViewSet.as_view({'get': 'list'})),
    path('news/', NewsViewSet.as_view({'get': 'list'})),
    path('collection/', CollectionViewSet.as_view({'get': 'list'})),
    path('new_product/', NewProductDetailViewSet.as_view({'get': 'list'})),
    path('favorites/', FavoriteProductDetailViewSet.as_view({'get': 'list'})),
    path('collection/<int:pk>/items/', CollectionDetailViewSet2.as_view({'get': 'list'})),
    path('collection/<int:pk>/', CollectionDetailViewSet.as_view({'get': 'retrieve'})),

    path('help/', HelpViewSet.as_view({'post': 'create'})),
    path('imagehelp/', HelpImageViewSet.as_view({'post': 'create'})),
    path('help/<int:pk>/', HelpViewSet.as_view({'put': 'update', 'get': 'retrieve'})),
    path('answers/', ApiView.as_view()),
    path('item/<int:pk>/similar/', SimilarItemViewSet.as_view({'get': 'list'})),
    path('item/<int:pk>/', ItemViewSet.as_view({'get': 'retrieve'})),

]
