# utils/decorators.py
# Role-based access control decorators - restricts access

from functools import wraps


def role_required(allowed_roles):
    """
    Generic role-based decorator.
    Ensures the current user has one of the allowed roles.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, current_user, *args, **kwargs):
            if not current_user:
                print("❌ Access denied. Please login first.")
                return None

            if current_user.role not in allowed_roles:
                print(
                    f"❌ Access denied. Role '{current_user.role}' not permitted.")
                return None

            return func(self, current_user, *args, **kwargs)
        return wrapper
    return decorator


# Specific decorators for cleaner usage
def admin_required(func):
    """Decorator for admin-only functions."""
    return role_required(["admin"])(func)


def health_worker_required(func):
    """Decorator for health worker or admin functions."""
    return role_required(["health_worker", "admin"])(func)


def community_required(func):
    """Decorator for community-only functions."""
    return role_required(["community"])(func)


def owner_required(func):
    """
    Ensures the current user is the owner of the resource.
    Expects the resource to be passed in kwargs as 'resource'.
    """
    @wraps(func)
    def wrapper(self, current_user, *args, **kwargs):
        resource = kwargs.get("resource")
        if not resource:
            print("❌ Access denied. No resource provided.")
            return None
        if resource.reported_by != current_user.id:
            print("❌ Access denied. You are not the owner of this resource.")
            return None
        return func(self, current_user, *args, **kwargs)
    return wrapper