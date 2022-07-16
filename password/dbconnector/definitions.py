import uuid
import datetime
from typing import TypedDict


class RawService(TypedDict):
    name: str
    url: str
    user: str
    password: str


class ServiceDict(RawService):
    password: bytes
    id: uuid.UUID
    utc_date: datetime.datetime


class DBCredentials(TypedDict):
    name: str
    user: str
    password: str
    host: str
    port: str
