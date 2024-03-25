from rest_framework import serializers

from post.models import Post
from product.models import Product


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'