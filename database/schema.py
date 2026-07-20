def create_tables(connection):

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            openalex_id TEXT UNIQUE NOT NULL,

            title TEXT NOT NULL,

            publication_date TEXT,

            citations INTEGER DEFAULT 0,

            doi TEXT,

            primary_url TEXT,

            search_query TEXT NOT NULL,

            collected_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            openalex_id TEXT UNIQUE,

            name TEXT NOT NULL

        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paper_authors (

            paper_id INTEGER NOT NULL,

            author_id INTEGER NOT NULL,

            author_position INTEGER,

            PRIMARY KEY (
                paper_id,
                author_id
            ),

            FOREIGN KEY (paper_id)
                REFERENCES papers(id),

            FOREIGN KEY (author_id)
                REFERENCES authors(id)

        )
    """)

    cursor.execute(
    """
    CREATE INDEX IF NOT EXISTS
    idx_papers_title
    ON papers(title)
    """
    )


    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_papers_search_query
        ON papers(search_query)
        """
    )


    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_papers_citations
        ON papers(citations)
        """
    )


    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_authors_name
        ON authors(name)
        """
    )

    connection.commit()