from rest_framework import serializers

from webapp.models import Advantages, Image, About_us, Help, ImageHelp, News, Collection, Item, ImageForItem


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
        serializer = ItemImageSerializer(ImageForItem.objects.filter(item_id=obj.pk), many=True)
        request = self.context.get('request')
        if not ImageForItem.objects.filter(item_id=obj.pk):
            return serializer.data
        else:
            list_of_data = []
            for i in serializer.data:
                dict_of_data = dict(i)
                dict_of_data['image'] = request.build_absolute_uri(dict_of_data['image'])
                list_of_data.append(dict_of_data)
            return list_of_data

    def get_item_collection(self, obj):
        serializer = CollectionSerializer(Collection.objects.filter(items_collection=obj.id), many=True)
        request = self.context.get('request')
        if not Collection.objects.filter(items_collection=obj.id):
            return serializer.data
        else:
            dict_of_data = dict(serializer.data[0])
            dict_of_data['image'] = request.build_absolute_uri(dict_of_data['image'])
            return dict_of_data


class SimilarItemSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'title', 'price', 'old_price', 'discount', 'product_size', 'favorite']


class SimilarItemSerializer(serializers.ModelSerializer):
    similar_items = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['similar_items']

    def get_similar_items(self, obj):
        request = self.context['request']
        a = Item.objects.get(pk=obj.id)
        b = Item.objects.filter(collection=a.collection).exclude(pk=obj.id)
        my_list = []
        serializer = SimilarItemSerializer2(b, many=True)
        list_of_data = []
        if serializer.data:
            for i in serializer.data:
                dict_of_data = dict(i)
                my_list.append({'images': ImageForItem.objects.filter(item_id=dict_of_data['id']), 'item': dict_of_data})
        for i in my_list:
            for j in i['images']:
                if j.image != request.build_absolute_uri(j.image):
                    j.image = request.build_absolute_uri(j.image.url)
                    j.save()
                else:
                    pass
            list_of_data.append({'images_for_item': i['images'].values('image', 'color'), 'item': i['item']})
        return {'sim': list_of_data}



