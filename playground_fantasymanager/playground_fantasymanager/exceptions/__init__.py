"""Custom exceptions for the application."""

from playground_fantasymanager.exceptions.base import AppError
from playground_fantasymanager.exceptions.handlers import register_exception_handlers

__all__ = ["AppError", "register_exception_handlers"]
