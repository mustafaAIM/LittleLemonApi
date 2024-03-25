from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from .models import Category, Cart, MenuItem, Order, OrderItem
from .serializers import MenuItemSerializer, ManagerUserSerializer, CartSerializer
from .permissions import IsManager, MenuItemPermissions, IsCustomer


class MenuItemListView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ["title", "category__title"]
    ordering_fields = ["title", "category__title", "price", "featured"]
    permission_classes = [MenuItemPermissions]


class MenuItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [MenuItemPermissions]


@api_view()
@permission_classes([IsManager])
def manager_view(request):
    return Response({"message": "Success"})


@api_view(["GET", "POST"])
@permission_classes([IsManager])
def manager_group_view(request):
    if request.method == "GET":
        users = User.objects.filter(groups__name="Manager")
        serialized = ManagerUserSerializer(users, many=True)
        return Response(serialized.data)

    elif request.method == "POST":
        username = request.data["username"]
        user = get_object_or_404(User, username=username)
        group = Group.objects.get(name="Manager")
        group.user_set.add(user)
        return Response(status=HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsManager])
def remove_manager_group(request, pk):
    user = get_object_or_404(User, pk=pk)
    manager_group = Group.objects.get(name="Manager")
    manager_group.user_set.remove(user)
    return Response(status=HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsManager])
def delivery_group_view(request):
    if request.method == "GET":
        users = User.objects.filter(groups__name="Delivery Crew")
        serialized = ManagerUserSerializer(users, many=True)
        return Response(serialized.data)

    elif request.method == "POST":
        username = request.data["username"]
        user = get_object_or_404(User, username=username)
        delivery_crew = Group.objects.get(name="Delivery Crew")
        delivery_crew.user_set.add(user)
        return Response(status=HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsManager])
def remove_delivery_group(request, pk):
    user = get_object_or_404(User, pk=pk)
    delivery_crew = Group.objects.get(name="Delivery Crew")
    delivery_crew.user_set.remove(user)
    return Response(status=HTTP_200_OK)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsCustomer])
def cart_manager_view(request):
    if request.method == "GET":
        carts = Cart.objects.filter(user=request.user)
        serialized = CartSerializer(carts, many=True)
        return Response(serialized.data)
    
    elif request.method == "POST":
        menu_item = MenuItem.objects.get(id=request.data["menu_item"])
        price = menu_item.price * int(request.data["quantity"])

        if Cart.objects.filter(user=request.user).exists():
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.create(user=request.user, quantity=request.data["quantity"], menuitem=menu_item, unit_price=menu_item.price, price=price)
        
        serialized = CartSerializer(cart)
        return Response(serialized.data, status=HTTP_201_CREATED)

    elif request.method == "DELETE":
        pass
