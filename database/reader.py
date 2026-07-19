def search_papers(
    connection,
    search_term,
    limit=10,
    sort_by="citations"
):

    search_pattern = (
        "%"
        + search_term
        + "%"
    )


    allowed_sort_columns = {

        "citations": (
            "papers.citations DESC"
        ),

        "date": (
            "papers.publication_date DESC"
        ),

        "title": (
            "papers.title ASC"
        )

    }


    if sort_by not in allowed_sort_columns:

        raise ValueError(
            "Invalid sort option"
        )


    order_by = (
        allowed_sort_columns[
            sort_by
        ]
    )


    cursor = connection.cursor()


    query = f"""
        SELECT DISTINCT
            papers.id,
            papers.openalex_id,
            papers.title,
            papers.publication_date,
            papers.citations,
            papers.doi,
            papers.primary_url,
            papers.search_query
        FROM papers
        LEFT JOIN paper_authors
            ON papers.id = paper_authors.paper_id
        LEFT JOIN authors
            ON paper_authors.author_id = authors.id
        WHERE
            papers.title LIKE ?
            OR authors.name LIKE ?
            OR papers.search_query LIKE ?
        ORDER BY
            {order_by}
        LIMIT ?
    """


    cursor.execute(
        query,
        (
            search_pattern,
            search_pattern,
            search_pattern,
            limit,
        )
    )


    return cursor.fetchall()


def get_authors_for_paper(
    connection,
    paper_id
):

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            authors.name,
            paper_authors.author_position
        FROM paper_authors
        JOIN authors
            ON paper_authors.author_id = authors.id
        WHERE paper_authors.paper_id = ?
        ORDER BY paper_authors.author_position
        """,
        (paper_id,)
    )


    return cursor.fetchall()