from fastapi import Request, Depends, HTTPException, status

from src.database.models import Role, User
from src.services.auth import auth_service


class RoleAccess:
    """
    A class to manage role-based access control in a FastAPI application.

    This class is designed to be used as a dependency in a FastAPI route.
    It uses the `auth_service.get_current_user` function to get the current user,
    and then checks if the user's role is in the list of allowed roles.

    :param allowed_roles: A list of roles that are allowed to access a specific resource.
    """

    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, user: User = Depends(auth_service.get_current_user)):
        """
        Check if the user's role is in the list of allowed roles.

        This method is designed to be used as a dependency in a FastAPI route.
        It uses the `auth_service.get_current_user` function to get the current user,
        and then checks if the user's role is in the list of allowed roles.

        :param request: The incoming request.
        :param user: The user obtained from the `auth_service.get_current_user` dependency.
        :raises HTTPException: If the user's role is not in the list of allowed roles.
        """

        print(user.role, self.allowed_roles)
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
