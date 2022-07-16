import logging
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cryptography.fernet import Fernet

from .modal import Service
from .definitions import RawService, DBCredentials


class DBConnector:
    def __init__(self, dbcred: DBCredentials, fernet_key: bytes, namespace: str) -> None:
        uri = "postgresql+psycopg2://"
        uri += f"{dbcred['user']}:{dbcred['password']}@"
        uri += f"{dbcred['host']}:{dbcred['port']}/{dbcred['name']}"
        engine = create_engine(uri)
        self.connection = sessionmaker(bind=engine)()
        self.logger = logging.getLogger("DBConnector")
        self.key = fernet_key
        self.fernet = Fernet(self.key)
        self.namespace = namespace

    def get_service(self, service_id: uuid.UUID) -> Service:
        return self.connection.query(Service).filter(Service.id == service_id).first()

    def list_services(self) -> list[dict[str, str]]:
        raw_list = self.connection.query(Service.id, Service.name).all()
        service_list = [item._asdict() for item in raw_list]
        print(service_list)
        return service_list

    def encrypt_password(self, password: str) -> bytes:
        return self.fernet.encrypt(password.encode())

    def decrypt_password(self, password: bytes) -> str:
        return self.fernet.decrypt(password).decode()

    def add_service(self, data: RawService) -> uuid.UUID:
        service_id = uuid.uuid5(uuid.UUID(self.namespace), f"{data['name']}:{data['user']}")
        service = Service(
            id=service_id,
            utc_date=datetime.now(),
            name=data["name"],
            url=data["url"],
            user=data["user"],
            password=self.encrypt_password(data["password"]),
        )
        self.connection.add(service)
        self.connection.commit()
        return service_id

    def delete_service(self, service_id: uuid.UUID):
        service = self.get_service(service_id)
        self.connection.delete(service)
        self.connection.commit()

    def update_service(self, service_id: uuid.UUID, data: RawService):
        service = self.get_service(service_id)
        service.name = data["name"]
        service.url = data["url"]
        service.user = data["user"]
        service.password = self.fernet.encrypt(data["password"].encode())
        self.connection.commit()
