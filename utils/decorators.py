def require_role(*allowed_roles):
    
    #Restricts function access based on user role

    def decorator(func):
        def wrapper(current_user, *args, **kwargs):
            if current_user.role not in allowed_roles:
                raise PermissionError("Access denied.")
            
            return func(current_user, *args, **kwargs)
        return wrapper
    return decorator