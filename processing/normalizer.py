def normalize_paper(paper, search_term):

    primary_location = (
        paper.get("primary_location")
        or {}
    )

    authors = []

    for position, authorship in enumerate(
        paper.get("authorships", [])
    ):

        author = authorship.get("author")

        if author:

            author_data = {
                "openalex_id": author.get("id"),
                "name": author.get("display_name"),
                "position": position
            }

            authors.append(author_data)

    return {
        "openalex_id": paper.get("id"),

        "title": paper.get(
            "title",
            "Untitled"
        ),

        "publication_date": paper.get(
            "publication_date"
        ),

        "citations": paper.get(
            "cited_by_count",
            0
        ),

        "doi": paper.get("doi"),

        "primary_url": primary_location.get(
            "landing_page_url"
        ),

        "search_query": search_term,

        "authors": authors
    }