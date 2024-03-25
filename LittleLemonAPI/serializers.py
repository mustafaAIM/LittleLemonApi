from rest_framework import serializers
from django.contrib.auth.models import User, Group

from .models import Category, Cart, MenuItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    # category_id = serializers.IntegerField(write_only=True)
    # category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class ManagerUserSerializer(serializers.ModelSerializer):
    # groups_id = serializers.IntegerField(write_only=True)
    # groups = GroupSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "groups"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
