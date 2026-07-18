from database.connection import get_connection


def test_database_connection():

    connection = get_connection(":memory:")

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE test (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO test (name)
        VALUES (?)
        """,
        ("Osama",)
    )

    result = cursor.execute(
        """
        SELECT name
        FROM test
        """
    ).fetchone()

    assert result[0] == "Osama"

    connection.close()