import sqlite3


DATABASE_PATH = "research.db"


def get_connection(database_path=DATABASE_PATH):

    connection = sqlite3.connect(
        database_path
    )

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection