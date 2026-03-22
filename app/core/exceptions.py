"""
Custom Exceptions

This module defines application-specific exceptions for better error handling.
"""


class AppException(Exception):
    """Base exception class for application errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    """Raised when a requested resource is not found."""

    def __init__(self, resource: str, resource_id: int | str):
        message = f"{resource} with id {resource_id} not found"
        super().__init__(message, status_code=404)


class PermissionDeniedError(AppException):
    """Raised when user doesn't have permission to access a resource."""

    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, status_code=403)


class ValidationError(AppException):
    """Raised when business logic validation fails."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class PortfolioNotFoundError(NotFoundError):
    """Raised when a portfolio is not found."""

    def __init__(self, portfolio_id: int):
        super().__init__("Portfolio", portfolio_id)


class TransactionNotFoundError(NotFoundError):
    """Raised when a transaction is not found."""

    def __init__(self, transaction_id: int):
        super().__init__("Transaction", transaction_id)


class PortfolioAccessDeniedError(PermissionDeniedError):
    """Raised when user tries to access a portfolio they don't own."""

    def __init__(self):
        super().__init__("You don't have permission to access this portfolio")


class TransactionAccessDeniedError(PermissionDeniedError):
    """Raised when user tries to access a transaction they don't own."""

    def __init__(self):
        super().__init__("You don't have permission to access this transaction")
