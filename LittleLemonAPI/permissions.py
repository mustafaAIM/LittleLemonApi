from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Validates that User is Logged in AND is part of Manager Group
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.groups.filter(name="Manager").exists())


class IsDeliveryCrew(BasePermission):
    """
    Validates that User is Logged In AND is part of Delivery Crew Group
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.groups.filter(name="Delivery crew").exists())


class IsCustomer(BasePermission):
    """
    Validates that User is Logged In AND is part of Customer Group
    """

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (
                not request.user.groups.filter(name="Manager").exists()
                and not request.user.groups.filter(name="Delivery Crew").exists()
            )
        )


class MenuItemPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return bool(request.user.is_authenticated)
        else:
            return bool(request.user.is_authenticated and request.user.groups.filter(name="Manager").exists())
