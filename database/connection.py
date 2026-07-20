import sqlite3

from config.settings import (
    DATABASE_PATH
)


def get_connection(
    database_path=None
):

    if database_path is None:

        database_path = (
            DATABASE_PATH
        )


    return sqlite3.connect(
        database_path
    )