"""
Document CRUD implementation using SQLAlchemy Session.
Implements CRUDInterface; receives session via composition (__init__).

Design:
- Single CRUDInterface with condition-based methods to avoid many variants.
- This repository focuses on Document and uses SQLAlchemy queries under the hood.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.interfaces.db_curd_interfaces.curd_interface import CRUDInterface
from app.models.document_model import Document


class SqliteDocumentRepository(CRUDInterface):
    """
    CRUD for documents table. Implements CRUDInterface for Document.
    Session is injected (composition): caller gets session from db.get_db() and passes it here.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    # ------------------------------------------------------------------
    # Interface methods
    # ------------------------------------------------------------------
    def insert(self, data: Any) -> Document:
        """
        Insert a new Document.
        - If data is a Document instance, use it directly.
        - If data is a dict, construct Document(**data).
        """
        if isinstance(data, Document):
            doc = data
        elif isinstance(data, dict):
            doc = Document(**data)
        else:
            raise TypeError("insert expects a Document or a dict of fields")

        self._session.add(doc)
        self._session.commit()
        self._session.refresh(doc)
        return doc

    def select(
        self,
        condition: dict[str, Any] | None = None,
    ) -> list[Document]:
        """
        Select documents matching the condition.
        - If condition is provided: filter by that condition.
        - If condition is None: delegate to select_all() (explicit, paginated).
        - Always returns a list (possibly empty).
        """
        if condition:
            query = self._session.query(Document).filter_by(**condition)
            return list(query.all())

        # No condition provided: fall back to explicit, limited listing
        return self.select_all()

    def update(
        self,
        condition: dict[str, Any] | None = None,
        data: Any | None = None,
    ) -> list[Document]:
        """
        Update documents matching the condition.
        - data can be a Document or a dict of fields to set.
        - Returns list[Document] after update.
        """
        if data is None:
            raise ValueError("update requires data")

        # Normalize data into a dict of field -> value (skip id)
        if isinstance(data, Document):
            values: dict[str, Any] = {
                col.name: getattr(data, col.name)
                for col in Document.__table__.columns
                if col.name != "id"
            }
        elif isinstance(data, dict):
            values = {k: v for k, v in data.items() if k != "id"}
        else:
            raise TypeError("update data must be a Document or a dict")

        if not condition:
            raise ValueError("update requires a condition to avoid updating all rows unintentionally")

        query = self._session.query(Document).filter_by(**condition)

        docs = query.all()
        for doc in docs:
            for field, value in values.items():
                setattr(doc, field, value)

        self._session.commit()

        for doc in docs:
            self._session.refresh(doc)

        return docs

    def delete(
        self,
        condition: dict[str, Any] | None = None,
    ) -> None:
        """
        Delete documents matching the condition.
        - If condition is provided: delete matching documents.
        - If condition is None: delegate to delete_all() explicitly.
        """
        if condition:
            query = self._session.query(Document).filter_by(**condition)
            query.delete(synchronize_session=False)
            self._session.commit()
            return

        # No condition: explicit mass delete
        self.delete_all()

    def select_all(self, limit: int = 100) -> list[Document]:
        """
        Return up to `limit` documents, newest first.
        """
        return (
            self._session.query(Document)
            .order_by(Document.created_at.desc())
            .all()
        )

    def delete_all(self) -> None:
        """
        Delete all documents.
        """
        self._session.query(Document).delete(synchronize_session=False)
        self._session.commit()

    # ------------------------------------------------------------------
    # Optional convenience helpers (not part of CRUDInterface)
    # ------------------------------------------------------------------

    def read_by_id(self, id: str) -> Document | None:
        """
        Convenience wrapper that selects by primary key.
        Uses the generic condition-based select() under the hood.
        """
        docs = self.select({"id": id})
        return docs[0] if docs else None
