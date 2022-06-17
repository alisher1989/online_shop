from django.http import JsonResponse
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Advantages, About_us, Help, ImageHelp, News, Collection, Item, ImageForItem, Public_offer, \
    Call_back, Slider, Order, BasketOrder
from webapp.serializers import AdvantagesSerializer, About_usSerializer, HelpSerializer, ImageHelpSerializer, \
    NewsSerializer, CollectionSerializer, ItemSerializer, ItemImageSerializer, SimilarItemSerializer, \
    FavoriteItemSerializer, PublicOfferSerializer, CallBackSerializer, SliderSerializer, \
    BasketOrderItemSerializer, TitleSearchSerializer
from rest_framework import pagination
import random
from rest_framework import filters


class CustomPaginationForNewItemsMainPage(pagination.PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'


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
    """Просмотр детального просмотра коллекции"""
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CustomPaginationForCollectionItems(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'


class CollectionDetailViewSet2(viewsets.ModelViewSet):
    """При просмотре определенной коллекции, будет показаны все товары из этой коллекции"""
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
        coll_id = Item.objects.get(pk=kwargs['pk']).collection_id
        item = Item.objects.get(pk=kwargs['pk'])
        items = Item.objects.filter(collection_id=coll_id).exclude(id=item.id)
        if items.count() > 5:
            queryset = items.order_by('-id')[:5]
        else:
            queryset = items
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
    """Список Новинок """
    queryset = Item.objects.filter(new_product=True).order_by('-id')
    serializer_class = SimilarItemSerializer

    def list(self, request, *args, **kwargs):
        if Item.objects.filter(new_product=True).order_by('-id').count() > 5:
            queryset = Item.objects.filter(new_product=True).order_by('-id')[:5]
        else:
            queryset = Item.objects.filter(new_product=True).order_by('-id')
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
    """Список Избранных товаров"""
    queryset = Item.objects.filter(favorite=True)
    serializer_class = FavoriteItemSerializer
    pagination_class = CustomPaginationForCollectionItems

    def list(self, request, *args, **kwargs):
        queryset = Item.objects.filter(favorite=True)
        collection = Collection.objects.all()
        random1 = []
        if not queryset:
            print('hhhh')
            if collection:
                for i in collection:
                    if i.items_collection.all():
                        random1.append({'k': i.items_collection.all()})
            l = []
            for i in random1:
                l.append(random.choice(list(i['k'])))
            queryset = l
            if len(l) > 5:
                queryset = l[:5]
        else:
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


class RandomProductDetailViewSet(viewsets.ModelViewSet):
    """Список рандомных товаров, если нет избранных"""
    queryset = Item.objects.all()
    serializer_class = SimilarItemSerializer

    def list(self, request, *args, **kwargs):
        queryset = Item.objects.filter(favorite=True)
        collection = Collection.objects.all()
        random1 = []
        if not queryset:
            print('hhhh')
            if collection:
                for i in collection:
                    if i.items_collection.all():
                        random1.append({'k': i.items_collection.all()})
            l = []
            for i in random1:
                l.append(random.choice(list(i['k'])))
            queryset = l
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(RandomProductDetailViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class PublicOfferViewSet(viewsets.ModelViewSet):
    """Публичная оферта"""
    queryset = Public_offer.objects.all()
    serializer_class = PublicOfferSerializer


class CallBackViewSet(viewsets.ModelViewSet):
    """Обратный звонок"""
    queryset = Call_back.objects.all()
    serializer_class = CallBackSerializer


class SliderViewSet(viewsets.ModelViewSet):
    """Обратный звонок"""
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer


class HitOfSalesViewSet(viewsets.ModelViewSet):
    """Список Новинок """
    queryset =Item.objects.filter(hit_of_sales=True).order_by('-id')
    serializer_class = SimilarItemSerializer
    pagination_class = CustomPaginationForNews

    def get_serializer_context(self):
        context = super(HitOfSalesViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class NewProductMainPageViewSet2(viewsets.ModelViewSet):
    """Список Новинок для главной страницы"""
    queryset =Item.objects.filter(new_product=True).order_by('-id')
    serializer_class = SimilarItemSerializer
    pagination_class = CustomPaginationForNews

    def get_serializer_context(self):
        context = super(NewProductMainPageViewSet2, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class OrderViewSet(ApiView):
    """Страница для заказа"""

    def post(self, request, *args, **kwargs):
        post1 = request.POST
        if kwargs:
            order = Order.objects.get(pk=kwargs['pk'])
        else:
            order = Order.objects.create(
                name=post1['name'],
                surname=post1['surname'],
                email=post1['email'],
                phone=post1['phone'],
                country=post1['country'],
                city=post1['city']
            )
        b = BasketOrder.objects.create(image=request.FILES['image'], basket=order, color=post1['color'],
                                       title=post1['title'], size=post1['size'], price=post1['price'],
                                       total_lines=post1['total_lines'], status=post1['status'],
                                       quantity_in_line=post1['quantity_in_line'])
        if not 'discount' in post1:
            pass
        elif post1['discount']:
            b.discount = post1['discount']
            Discounted_Price = int(post1['price']) - (100 * (int(post1['discount'])) / 100)
            b.old_price = int(Discounted_Price)
            b.save()
        return Response(status=status.HTTP_201_CREATED, data={'object': 'successfully created'})

    def get(self, request, *args, **kwargs):
        tutorials = BasketOrder.objects.all()
        tutorials_serializer = BasketOrderItemSerializer(tutorials, many=True, context={'request': request})
        return Response(tutorials_serializer.data, 200)

    def delete(self, request, pk, **kwargs):
        try:
            Order.objects.get(pk=pk).delete()
            return Response({'delete': 'successfully deleted'})
        except:
            return Response({'delete': 'There is no object with this PK'})


class OrderDeleteViewSet(ApiView):
    """Страница для заказа"""

    def delete(self, request, pk):
        try:
            BasketOrder.objects.get(pk=pk).delete()
            return Response({'delete': 'successfully deleted'})
        except:
            return Response({'delete': 'There is no object with this PK'})




class QuestionsAPIView(viewsets.ModelViewSet):
    pagination_class = CustomPaginationForNews
    serializer_class = SimilarItemSerializer
    queryset = Item.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Item.objects.filter(title__icontains=request.GET['search'])
        page = self.paginate_queryset(queryset)
        collection = Collection.objects.all()
        random1 = []
        if not queryset:
            if collection:
                for i in collection:
                    if i.items_collection.all():
                        random1.append({'collection_items': i.items_collection.all()})
            l = []
            for i in random1:
                l.append(random.choice(list(i['collection_items'])))
            queryset = l
            if len(l) > 5:
                queryset = l[:5]
        else:
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = SimilarItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class TitleSearchView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = TitleSearchSerializer

    def list(self, request, *args, **kwargs):
        queryset = Item.objects.filter(title__icontains=request.GET['search'])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

