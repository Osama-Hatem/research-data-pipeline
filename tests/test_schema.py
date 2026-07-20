from database.connection import get_connection
from database.schema import create_tables


def test_create_tables_creates_indexes():

    connection = get_connection(
        ":memory:"
    )


    create_tables(
        connection
    )


    indexes = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'index'
        """
    ).fetchall()


    index_names = [

        index[0]

        for index in indexes

    ]


    assert (
        "idx_papers_title"
        in index_names
    )


    assert (
        "idx_papers_search_query"
        in index_names
    )


    assert (
        "idx_papers_citations"
        in index_names
    )


    assert (
        "idx_authors_name"
        in index_names
    )


    connection.close()