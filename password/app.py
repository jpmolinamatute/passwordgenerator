#! /usr/bin/env python

import sys
import logging
from os import path, environ

from dotenv import load_dotenv

from password.dbconnector import DBConnector, DBCredentials
from password.passwordgenerator import PasswordGenerator


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Script %s has started", path.basename(__file__))
    load_dotenv()
    cred: DBCredentials = {
        "name": environ["DB_NAME"],
        "user": environ["DB_USER"],
        "password": environ["DB_PASSWORD"],
        "host": environ["DB_HOST"],
        "port": environ["DB_PORT"],
    }
    db = DBConnector(cred, environ["FERNET_KEY"].encode(), environ["NAMESPACE"])
    passgen = PasswordGenerator(min_patter=2, length=20)
    password = passgen.generate()
    logging.info("Password generated: %s", password)
    # service_id = db.add_service(
    #     {
    #         "name": "Test12",
    #         "url": "https://test.com",
    #         "user": "test12",
    #         "password": password,
    #     }
    # )

    # logging.info(service_list)
    # service = db.get_service(service_id)
    db.list_services()
    # logging.info(service)
    # logging.info(db.decrypt_password(service["password"]))
    # logging.info(service)


if __name__ == "__main__":
    EXIT_STATUS = 0
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Bye!")
    except Exception as e:
        logging.exception(e)
        EXIT_STATUS = 2
    finally:
        sys.exit(EXIT_STATUS)
