"""
module with utilities for interaction with PostgreSQL database
"""

from collections import UserDict
import os
import psycopg2


class Credentials(UserDict):
    """
    - to be populated with credentials for connecting to PostgreSQL db
    - usage: psycopg2.connect(**Credentials(*args, **kwargs))
    - if credentials for user and password are not provided, they will be taken
      from environment variables (env variables → postgres_user + postgres_pwd)
    - if env variables are not set, default values will be used (user=postgres, password=postgres)
    - defaults for host, port = localhost, 5432
    """

    def __init__(self, database, host="localhost", port=5432, user=None, password=None):
        user = user if user is not None else os.getenv("postgres_user", "postgres")
        password = password if password is not None else os.getenv("postgres_pwd", "postgres")

        super().__init__(
            database=database,
            host=host,
            port=port,
            user=user,
            password=password,
        )

    def __repr__(self):
        hide_if_pwd = lambda k, v: (k, "***") if k == "password" else (k, v)
        return str(dict(hide_if_pwd(*item) for item in vars(self)["data"].items()))
