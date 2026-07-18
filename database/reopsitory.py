from database.connection import get_connection


def save_paper(paper, connection):

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO papers (
            openalex_id,
            title,
            publication_date,
            citations,
            doi,
            primary_url,
            search_query
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            paper["openalex_id"],
            paper["title"],
            paper["publication_date"],
            paper["citations"],
            paper["doi"],
            paper["primary_url"],
            paper["search_query"]
        )
        )

    paper_id = cursor.execute(
        """
        SELECT id
        FROM papers
        WHERE openalex_id = ?
        """,
        (paper["openalex_id"],)
    ).fetchone()[0]


    for author in paper["authors"]:

        cursor.execute(
            """
            INSERT OR IGNORE INTO authors (
                openalex_id,
                name
            )
            VALUES (?, ?)
            """,
            (
                author["openalex_id"],
                author["name"]
            )
        )


        author_id = cursor.execute(
            """
            SELECT id
            FROM authors
            WHERE openalex_id = ?
            """,
            (author["openalex_id"],)
        ).fetchone()[0]


        cursor.execute(
            """
            INSERT OR IGNORE INTO paper_authors (
                paper_id,
                author_id,
                author_position
            )
            VALUES (?, ?, ?)
            """,
            (
                paper_id,
                author_id,
                author["position"]
            )
        )