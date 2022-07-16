import uuid

from sqlalchemy import Column, DateTime, String, UniqueConstraint, LargeBinary
from sqlalchemy.orm import Mapped
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from .definitions import ServiceDict

Base = declarative_base()


class Service(Base):
    __tablename__ = "service"
    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True)
    utc_date = Column(DateTime(timezone=False), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    user = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    __table_args__ = (UniqueConstraint("name", "user", name="_name_user_uc"),)

    def _asdict(self) -> ServiceDict:
        # return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        return {
            "name": getattr(self, "name"),
            "url": getattr(self, "url"),
            "user": getattr(self, "user"),
            "password": getattr(self, "password"),
            "id": getattr(self, "id"),
            "utc_date": getattr(self, "utc_date"),
        }

    def __repr__(self):
        # class_ = self.__class__.__name__
        # attrs: list[tuple[str, str]] = sorted((k, getattr(self, k)) for k in self.__mapper__.columns.keys())
        # sattrs = ", ".join(f"{x[0]}={x[1]}" for x in attrs)
        # return f"{class_}({sattrs})"
        asdict = self._asdict()
        password = "*****"  # asdict["password"].decode()
        utc_date = asdict["utc_date"].strftime("%Y/%m/%d %H:%M:%S")
        fmt = "Service("
        fmt += f"id={asdict['id']}, name={asdict['name']}, url={asdict['url']}, user={asdict['user']}, "
        fmt += f"{password=} {utc_date=}"
        return fmt
