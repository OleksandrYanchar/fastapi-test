import uuid
from datetime import datetime
from typing import Annotated, Optional

from sqlalchemy import Integer, String, text
from sqlalchemy.orm import mapped_column

uuidpk = Annotated[
    uuid.UUID,
    mapped_column(primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
]
intpk = Annotated[
    Integer,
    mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False),
]


created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]

updated_at = Annotated[
    Optional[datetime], mapped_column(default=None, onupdate=datetime.utcnow)
]

unique_str_64 = Annotated[str, mapped_column(String(64), nullable=False, unique=True)]
