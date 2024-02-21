from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from .models import Post, Category


class CategorySerializer(PrimaryKeyRelatedField, ModelSerializer):
    class Meta:
        model = Category


class PostSerializer(ModelSerializer):
    author = serializers.CharField(read_only=True)
    category = CategorySerializer(many=True, queryset=Category.objects.all())
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'heading', 'text', 'category', 'created', 'author', 'rating']
