from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Advantages, About_us, Help, ImageHelp, News, Collection, Item, ImageForItem
from webapp.serializers import AdvantagesSerializer, About_usSerializer, HelpSerializer, ImageHelpSerializer, \
    NewsSerializer, CollectionSerializer, ItemSerializer


class AdvantagesViewSet(viewsets.ModelViewSet):
    """Список преимуществ"""
    queryset = Advantages.objects.all()
    serializer_class = AdvantagesSerializer


class About_usViewSet(viewsets.ModelViewSet):
    """Инфо о нас"""
    queryset = About_us.objects.all()
    serializer_class = About_usSerializer


class HelpViewSet(viewsets.ModelViewSet):
    """Инфо о нас"""
    queryset = Help.objects.all()
    serializer_class = HelpSerializer


class ApiView(APIView):
    """Endpoint для получения одного фото и всех вопрос/ответов"""
    def get(self, request, *args, **kwargs):
        tutorials = ImageHelp.objects.all()
        tutorials_serializer = ImageHelpSerializer(tutorials, many=True)
        h = Help.objects.all()
        other = HelpSerializer(h, many=True)
        return JsonResponse({'image_of_help': tutorials_serializer.data, 'questions_answers': other.data}, safe=False)


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


from rest_framework import pagination


class CustomPaginationForNews(pagination.PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'


class NewsViewSet(viewsets.ModelViewSet):
    """Список новостей"""
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = CustomPaginationForNews


class CollectionViewSet(viewsets.ModelViewSet):
    """Список новостей"""
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = CustomPaginationForNews


class ItemViewSet(viewsets.ModelViewSet):
    """Инфо детального просмотра Товара"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_serializer_context(self):
        context = super(ItemViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)




