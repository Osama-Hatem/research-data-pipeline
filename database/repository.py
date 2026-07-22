def save_paper(
    paper,
    connection
):

    cursor = connection.cursor()


    try:

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
                paper["search_query"],
            ),
        )


        was_inserted = (
            cursor.rowcount == 1
        )


        paper_row = cursor.execute(
            """
            SELECT id
            FROM papers
            WHERE openalex_id = ?
            """,
            (
                paper["openalex_id"],
            ),
        ).fetchone()


        paper_id = paper_row[0]


        for author in paper["authors"]:

            if not author["openalex_id"]:

                continue


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
                    author["name"],
                ),
            )


            author_row = cursor.execute(
                """
                SELECT id
                FROM authors
                WHERE openalex_id = ?
                """,
                (
                    author["openalex_id"],
                ),
            ).fetchone()


            author_id = author_row[0]


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
                    author["position"],
                ),
            )


        connection.commit()


        return was_inserted


    except Exception:

        connection.rollback()

        raise