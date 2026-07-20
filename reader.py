import argparse

from database.connection import get_connection
from database.reader import (
    search_papers,
    get_authors_for_paper
)
from config.settings import (
    DEFAULT_SEARCH_LIMIT
)
from database.reader import (
    search_papers,
    get_authors_for_paper,
    get_database_statistics,
    get_recent_papers,
    search_authors,
    get_papers_for_author,
    get_top_cited_papers
)


def search_and_print(
    search_term,
    limit=DEFAULT_SEARCH_LIMIT,
    sort_by="citations"
):

    connection = get_connection()


    try:

        papers = search_papers(
            connection,
            search_term,
            sort_by,
            limit=DEFAULT_SEARCH_LIMIT
        )


        if not papers:

            print(
                "No papers found."
            )

            return


        print(
            f"Found {len(papers)} paper(s)"
        )


        for paper in papers:

            print_paper(
                connection,
                paper
            )


    finally:

        connection.close()

def print_statistics():

    connection = get_connection()


    try:

        statistics = (
            get_database_statistics(
                connection
            )
        )


        print()

        print(
            "Research Database Statistics"
        )

        print(
            "----------------------------"
        )


        print(
            "Papers:",
            statistics["papers"]
        )


        print(
            "Authors:",
            statistics["authors"]
        )


        print(
            "Paper-author relationships:",
            statistics["relationships"]
        )


        print(
            "Average citations:",
            round(
                statistics[
                    "average_citations"
                ],
                2
            )
        )


    finally:

        connection.close()

def print_recent_papers(
    limit=DEFAULT_SEARCH_LIMIT
):

    connection = get_connection()


    try:

        papers = get_recent_papers(
            connection,
            limit=DEFAULT_SEARCH_LIMIT
        )


        if not papers:

            print(
                "No papers found."
            )

            return


        print(
            f"Recently collected "
            f"{len(papers)} paper(s)"
        )


        for paper in papers:

            print()

            print(
                "Title:",
                paper[2]
            )

            print(
                "Publication date:",
                paper[3]
            )

            print(
                "Citations:",
                paper[4]
            )

            print(
                "Collected at:",
                paper[8]
            )

            print(
                "--------------------"
            )


    finally:

        connection.close()

def search_and_print_authors(
    search_term,
    limit=DEFAULT_SEARCH_LIMIT
):

    connection = get_connection()

    try:

        authors = search_authors(
            connection,
            search_term,
            limit=DEFAULT_SEARCH_LIMIT
        )

        if not authors:

            print(
                "Author not found"
            )

            return

        print(
            f"Found {len(authors)} author(s)"
        )

        for author in authors:

            author_id = author[0]

            openalex_id = author[1]

            name = author[2]

            print()

            print(
                "Name:",
                name,
            )

            print(
                "OpenAlex ID:",
                openalex_id,
            )

            print(
                "Author ID:",
                author_id,
            )

            print(
                "--------------------"
            )

    finally:

        connection.close()

def print_top_cited_papers(
    limit=DEFAULT_SEARCH_LIMIT
):

    connection = get_connection()


    try:

        papers = get_top_cited_papers(
            connection,
            limit=DEFAULT_SEARCH_LIMIT
        )


        if not papers:

            print(
                "No papers found."
            )

            return


        print(
            f"Top {len(papers)} "
            "most-cited paper(s)"
        )


        for index, paper in enumerate(
            papers,
            start=1
        ):

            print()

            print(
                f"{index}. {paper[2]}"
            )

            print(
                "   Citations:",
                paper[4]
            )

            print(
                "   Publication date:",
                paper[3]
            )

            print(
                "   DOI:",
                paper[5]
            )

            print(
                "--------------------"
            )


    finally:

        connection.close()
        

def print_paper(
    connection,
    paper
):

    paper_id = paper[0]

    openalex_id = paper[1]

    title = paper[2]

    publication_date = paper[3]

    citations = paper[4]

    doi = paper[5]

    primary_url = paper[6]

    search_query = paper[7]


    authors = get_authors_for_paper(
        connection,
        paper_id
    )


    print()

    print(
        "Title:",
        title
    )

    print(
        "OpenAlex ID:",
        openalex_id
    )

    print(
        "Date:",
        publication_date
    )

    print(
        "Citations:",
        citations
    )

    print(
        "DOI:",
        doi
    )

    print(
        "URL:",
        primary_url
    )

    print(
        "Collected from search:",
        search_query
    )


    print(
        "Authors:"
    )


    if not authors:

        print(
            "  No authors found"
        )

    else:

        for author in authors:

            name = author[0]

            position = author[1]


            print(
                f"  {position + 1}. {name}"
            )


    print(
        "--------------------"
    )


def positive_integer(
    value
):

    value = int(
        value
    )


    if value <= 0:

        raise argparse.ArgumentTypeError(
            "limit must be greater than zero"
        )


    return value


def create_parser():

    parser = argparse.ArgumentParser(
        description=(
            "Search collected research papers"
        )
    )


    parser.add_argument(
        "search_term",
        nargs="+",
        help=(
            "Term to search for in "
            "paper titles, authors, "
            "or search queries"
        )
    )


    parser.add_argument(
        "--limit",
        type=positive_integer,
        default=DEFAULT_SEARCH_LIMIT,
        help=(
            "Maximum number of papers "
            "to display "
            f"(default: {DEFAULT_SEARCH_LIMIT})"
        )
    )


    parser.add_argument(
        "--sort",
        choices=[
            "citations",
            "date",
            "title"
        ],
        default="citations",
        help=(
            "Sort results by citations, "
            "date, or title "
            "(default: citations)"
        )
    )


    return parser


def main():

    parser = create_parser()


    args = parser.parse_args()


    search_term = " ".join(
        args.search_term
    )


    search_and_print(
        search_term,
        args.limit,
        args.sort
    )

if __name__ == "__main__":

    main()