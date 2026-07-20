from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session

from .helpers import normalize_name


class HasName(Protocol):
    name: Mapped[str]


def create_or_get[T: HasName](db: Session, model: type[T], name: str) -> T:
    # Query-then-insert has a race; unreachable on a single-writer deployment;
    # harden with ON CONFLICT or a savepoint if multi-user

    name = normalize_name(name)
    query = select(model).where(model.name == name)
    result = db.scalars(query).first()
    if result is not None:
        return result
    obj = model()
    obj.name = name
    db.add(obj)
    db.flush()
    return obj
