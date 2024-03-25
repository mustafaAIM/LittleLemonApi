from django.urls import path

from . import views

urlpatterns = [
    path("menu-items", views.MenuItemListView.as_view()),
    path("menu-items/<int:pk>", views.MenuItemRetrieveUpdateDestroyView.as_view()),
    path("groups/manager/users", views.manager_group_view),
    path("groups/manager/users/<int:pk>", views.remove_manager_group),
    path("groups/delivery-crew/users", views.delivery_group_view),
    path("groups/delivery-crew/users/<int:pk>", views.remove_delivery_group),
    path("cart/menu-items", views.cart_manager_view),
]
