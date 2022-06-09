from rest_framework import serializers
from webapp.models import Advantages, Image, About_us, Help, ImageHelp, News, Collection


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
    class Meta:
        model = ImageHelp
        fields = ['image']


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



