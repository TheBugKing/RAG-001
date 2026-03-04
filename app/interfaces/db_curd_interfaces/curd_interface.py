"""
Abstract CRUD interface (generic, condition-based).

One interface for all repositories:
- insert(data)
- select(condition)
- update(condition, data)
- delete(condition)
- select_all(limit)
- delete_all()
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CRUDInterface(ABC):
    """
    Generic CRUD contract.
    Repositories are free to interpret `data` (e.g. ORM model or dict)
    and `condition` (e.g. {"id": "...", "status": "pending"}).
    """

    @abstractmethod
    def insert(self, data: Any) -> Any:
        """Insert a new record. Returns the created record."""
        ...

    @abstractmethod
    def select(
        self,
        condition: dict[str, Any] | None = None,
    ) -> list[Any]:
        """
        Select records matching the condition.
        - If condition is None: select all (use with care).
        - Always returns a list (possibly empty).
        """
        ...

    @abstractmethod
    def update(
        self,
        condition: dict[str, Any] | None = None,
        data: Any | None = None,
    ) -> list[Any]:
        """
        Update records matching the condition.
        - `data` describes fields to change.
        - Returns the list of updated records.
        """
        ...

    @abstractmethod
    def delete(
        self,
        condition: dict[str, Any] | None = None,
    ) -> None:
        """
        Delete records matching the condition.
        - If condition is None: delete all (use with care).
        """
        ...

    @abstractmethod
    def select_all(self) -> list[Any]:
        """List all records (repository defines ordering)."""
        ...

    @abstractmethod
    def delete_all(self) -> None:
        """Delete all records."""
        ...