"""Base exception classes."""

from typing import Any, Optional


class AppError(Exception):
    """Base application exception."""

    def __init__(
        self,
        code: str,
        status_code: int,
        message: str,
        description: str = "",
    ) -> None:
        self.code = code
        self.status_code = status_code
        self.message = message
        self.description = description
        super().__init__(self.message)


class ValidationError(AppError):
    """Validation error exception."""

    def __init__(
        self,
        message: str,
        description: str = "",
        field: Optional[str] = None,
    ) -> None:
        self.field = field
        super().__init__(
            code="VALIDATION_ERROR",
            status_code=422,
            message=message,
            description=description,
        )


class NotFoundError(AppError):
    """Resource not found exception."""

    def __init__(
        self,
        message: str,
        description: str = "",
        resource_type: Optional[str] = None,
        resource_id: Optional[Any] = None,
    ) -> None:
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(
            code="NOT_FOUND",
            status_code=404,
            message=message,
            description=description,
        )


class ConflictError(AppError):
    """Resource conflict exception."""

    def __init__(
        self,
        message: str,
        description: str = "",
    ) -> None:
        super().__init__(
            code="CONFLICT",
            status_code=409,
            message=message,
            description=description,
        )


class AuthenticationError(AppError):
    """Authentication error exception."""

    def __init__(
        self,
        message: str = "Authentication required",
        description: str = (
            "Valid authentication credentials are required to access this resource"
        ),
    ) -> None:
        super().__init__(
            code="AUTHENTICATION_REQUIRED",
            status_code=401,
            message=message,
            description=description,
        )


class AuthorizationError(AppError):
    """Authorization error exception."""

    def __init__(
        self,
        message: str = "Insufficient permissions",
        description: str = (
            "You do not have sufficient permissions to access this resource"
        ),
    ) -> None:
        super().__init__(
            code="INSUFFICIENT_PERMISSIONS",
            status_code=403,
            message=message,
            description=description,
        )
