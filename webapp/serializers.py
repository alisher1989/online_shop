from rest_framework import serializers
from webapp.models import Advantages, Image, About_us, Help, ImageHelp


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



