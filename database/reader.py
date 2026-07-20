from config.settings import DEFAULT_SEARCH_LIMIT

def search_papers(
    connection,
    search_term,
    limit=DEFAULT_SEARCH_LIMIT,
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

def get_database_statistics(
    connection
):

    paper_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM papers
        """
    ).fetchone()[0]


    author_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM authors
        """
    ).fetchone()[0]


    relationship_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM paper_authors
        """
    ).fetchone()[0]


    average_citations = connection.execute(
        """
        SELECT AVG(citations)
        FROM papers
        """
    ).fetchone()[0]


    return {

        "papers": paper_count,

        "authors": author_count,

        "relationships":
        relationship_count,

        "average_citations":
        average_citations or 0

    }

def get_recent_papers(
    connection,
    limit=DEFAULT_SEARCH_LIMIT
):

    return connection.execute(
        """
        SELECT
            id,
            openalex_id,
            title,
            publication_date,
            citations,
            doi,
            primary_url,
            search_query,
            collected_at
        FROM papers
        ORDER BY collected_at DESC, id DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

def search_authors(
    connection,
    search_term,
    limit=DEFAULT_SEARCH_LIMIT
):

    return connection.execute(
        """
        SELECT
            id,
            openalex_id,
            name
        FROM authors
        WHERE name LIKE ?
        ORDER BY name
        LIMIT ?
        """,
        (
            f"%{search_term}%",
            limit
        )
    ).fetchall()

def get_papers_for_author(
    connection,
    author_id
):

    return connection.execute(
        """
        SELECT
            papers.id,
            papers.openalex_id,
            papers.title,
            papers.publication_date,
            papers.citations
        FROM papers
        JOIN paper_authors
            ON papers.id = paper_authors.paper_id
        WHERE paper_authors.author_id = ?
        ORDER BY papers.citations DESC
        """,
        (
            author_id,
        )
    ).fetchall()

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

def get_top_cited_papers(
    connection,
    limit=DEFAULT_SEARCH_LIMIT
):

    return connection.execute(
        """
        SELECT
            id,
            openalex_id,
            title,
            publication_date,
            citations,
            doi,
            primary_url,
            search_query
        FROM papers
        ORDER BY citations DESC, id ASC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

