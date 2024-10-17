from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'author'):
            return obj.author == request.user or request.user.is_staff
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_staff
        return False
    
class CustomQuestionPermission(permissions.BasePermission):
    """
    Custom permission to allow:
    - Anyone to read (GET, HEAD, OPTIONS)
    - Authenticated users to create (POST)
    - Owners to update (PUT, PATCH)
    - Admins to delete (DELETE)
    """

    def has_permission(self, request, view):
        print(f"HAS PERMISSION SECTION: Request User: {request.user}, Is authenticated: {request.user.is_authenticated}, Methode: {request.method}")
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        print(f"HAS OBJECT PERMISSION SECTION: Author: {obj.author}, Request User: {request.user}, Is Staff: {request.user.is_staff}, Methode: {request.method}")
        if request.method in permissions.SAFE_METHODS:
            print('SAFE_METHODS ABSCHNITT')
            return True
        elif request.method in ['PUT', 'PATCH']:
            print('PUT PATCH ABSCHNITT')
            return obj.author == request.user or request.user.is_staff
        elif request.method == 'DELETE':
            return request.user.is_staff
        return False