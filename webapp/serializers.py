from rest_framework import serializers

from webapp.models import Advantages, Image, About_us, Help, ImageHelp, News, Collection, Item, ImageForItem, \
    Public_offer, Call_back, Slider, Order, BasketOrder, FooterHeader, Connect


class AdvantagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advantages
        fields = ['image', 'header', 'description']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class About_usSerializer(serializers.ModelSerializer):
   images = ImageSerializer(many=True)

   class Meta:
        model = About_us
        fields = ['header', 'description', 'images']


class ImageHelpSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageHelp
        fields = ['photo_url']

    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.image.url
        return request.build_absolute_uri(photo_url)


class HelpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Help
        fields = ['questions', 'answers']


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ['image', 'title', 'description']


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'image', 'title']


class ItemImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageForItem
        fields = ['image', 'color', 'item']


class ItemSerializer(serializers.ModelSerializer):
    item_images = serializers.SerializerMethodField()
    item_collection = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['item_images', 'item_collection', 'title', 'article', 'price', 'old_price', 'discount', 'description', 'product_size', 'fabric_structure',
                  'quantity_in_line', 'material', 'hit_of_sales', 'new_product']

    def get_item_images(self, obj):
        serializer = ItemImageSerializer(ImageForItem.objects.filter(item_id=obj.pk), many=True, context={'request': self.context['request']})
        return serializer.data

    def get_item_collection(self, obj):
        serializer = CollectionSerializer(Collection.objects.filter(items_collection=obj.id), many=True, context={'request': self.context['request']})
        return serializer.data


class SimilarItemSerializer(serializers.ModelSerializer):
    item_images = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'item_images', 'title', 'price', 'old_price', 'discount', 'product_size', 'favorite']

    def get_item_images(self, obj):
        serializer = ItemImageSerializer(ImageForItem.objects.filter(item_id=obj.pk), many=True, context={'request': self.context['request']})
        return serializer.data


class FavoriteItemSerializer(serializers.ModelSerializer):
    item_images = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'item_images', 'discount', 'title', 'price', 'old_price', 'discount', 'product_size', 'favorite', 'count']

    def get_item_images(self, obj):
        serializer = ItemImageSerializer(ImageForItem.objects.filter(item_id=obj.pk), many=True, context={'request': self.context['request']})
        return serializer.data

    def get_count(self, obj):
        return {'count_of_favorites': self.context['count']}


class CollectionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'title', 'price', 'old_price', 'discount', 'product_size', 'favorite']


class PublicOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Public_offer
        exclude = []


class CallBackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call_back
        fields = ['name', 'phone']


class SliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slider
        exclude = []


class BasketOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasketOrder
        fields = ['image', 'title', 'quantity_in_line', 'color', 'price', 'total_products']


class TitleSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'title']


class HeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = FooterHeader
        exclude = []


class ConnectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connect
        exclude = ['type_of_connect']