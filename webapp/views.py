from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Advantages, About_us, Help, ImageHelp, News, Collection, Item, ImageForItem
from webapp.serializers import AdvantagesSerializer, About_usSerializer, HelpSerializer, ImageHelpSerializer, \
    NewsSerializer, CollectionSerializer, ItemSerializer, ItemImageSerializer, SimilarItemSerializer, \
    FavoriteItemSerializer
from rest_framework import pagination



class AdvantagesViewSet(viewsets.ModelViewSet):
    """Список преимуществ"""
    queryset = Advantages.objects.all()
    serializer_class = AdvantagesSerializer


class About_usViewSet(viewsets.ModelViewSet):
    """Инфо о нас"""
    queryset = About_us.objects.all()
    serializer_class = About_usSerializer


class HelpViewSet(viewsets.ModelViewSet):
    """Инфо о помощи"""
    queryset = Help.objects.all()
    serializer_class = HelpSerializer


class ApiView(APIView):
    """Endpoint для получения одного фото и всех вопрос/ответов"""
    def get(self, request, *args, **kwargs):
        tutorials = ImageHelp.objects.all()
        tutorials_serializer = ImageHelpSerializer(tutorials, many=True,  context={'request': request})
        h = Help.objects.all()
        other = HelpSerializer(h, many=True)
        response = {'image_of_help': tutorials_serializer.data, 'questions_answers': other.data}
        return Response(response, 200)


class HelpImageViewSet(viewsets.ModelViewSet):
    """Добавить фото для главы 'Помощь'"""
    queryset = ImageHelp.objects.all()
    serializer_class = ImageHelpSerializer

    def create(self, request, *args, **kwargs):
        ImageHelp.objects.get(pk=1).delete()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(data=serializer.data, status=status.HTTP_201_CREATED)


class CustomPaginationForNews(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'


class NewsViewSet(viewsets.ModelViewSet):
    """Список новостей"""
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = CustomPaginationForNews


class CollectionViewSet(viewsets.ModelViewSet):
    """Список коллекции"""
    queryset = Collection.objects.all()
    pagination_class = CustomPaginationForNews
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        context = super(CollectionViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class CollectionDetailViewSet(viewsets.ModelViewSet):
    """Список коллекции"""
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CustomPaginationForCollectionItems(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'


class CollectionDetailViewSet2(viewsets.ModelViewSet):
    """Список коллекции"""
    queryset = Item.objects.all()
    serializer_class = SimilarItemSerializer
    pagination_class = CustomPaginationForCollectionItems

    def list(self, request, *args, **kwargs):
        queryset = Item.objects.filter(collection_id=kwargs['pk'])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(CollectionDetailViewSet2, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class ItemViewSet(viewsets.ModelViewSet):
    """Инфо детального просмотра Товара"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_serializer_context(self):
        context = super(ItemViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class SimilarItemViewSet(viewsets.ModelViewSet):
    """Похожие товары"""
    queryset = Item.objects.all()
    serializer_class = SimilarItemSerializer

    def list(self, request, *args, **kwargs):
        if Item.objects.filter(collection_id=kwargs['pk']).count() > 5:
            queryset = Item.objects.filter(collection_id=kwargs['pk'])[-5:]
        else:
            queryset = Item.objects.filter(collection_id=kwargs['pk'])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(SimilarItemViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class NewProductDetailViewSet(viewsets.ModelViewSet):
    """Список коллекции"""
    queryset = Item.objects.all()
    serializer_class = SimilarItemSerializer

    def list(self, request, *args, **kwargs):
        queryset = Item.objects.filter(new_product=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(NewProductDetailViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class FavoriteProductDetailViewSet(viewsets.ModelViewSet):
    """Список коллекции"""
    queryset = Item.objects.all()
    serializer_class = FavoriteItemSerializer
    pagination_class = CustomPaginationForCollectionItems

    def list(self, request, *args, **kwargs):
        queryset = Item.objects.filter(favorite=True)
        print(queryset.count())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(FavoriteProductDetailViewSet, self).get_serializer_context()
        context.update({"request": self.request, 'count': Item.objects.filter(favorite=True).count()})
        return context






