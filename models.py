import os

import datetime

from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from sqlalchemy import create_engine, Integer, String, DateTime, func

POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ad_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", '5431')


engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
                       f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Ads(Base):
    __tablename__ = "all_ads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "owner": self.owner,
        }


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

