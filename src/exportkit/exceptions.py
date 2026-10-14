"""Exception hierarchy for exportkit."""

from __future__ import annotations


class ExportKitError(Exception):
    """Base class for every error raised by exportkit."""


class UnsupportedFormatError(ExportKitError):
    """Raised when a requested output format is not supported."""


class MissingDependencyError(ExportKitError):
    """Raised when the optional dependency for a format is not installed."""
