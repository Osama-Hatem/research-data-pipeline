import argparse

from scrapper import collect_papers
from reader import (
    search_and_print,
    print_statistics,
    print_recent_papers,
    positive_integer,
    search_and_print_authors,
    print_top_cited_papers
)
from config.settings import DEFAULT_SEARCH_LIMIT
from database.exporter import (
    export_papers_to_csv,
    export_papers_to_json
)
from database.connection import get_connection

def handle_search(
    args
):

    search_term = " ".join(
        args.search_term
    )


    search_and_print(
        search_term,
        args.limit,
        args.sort
    )

def handle_stats():

    print_statistics()

def handle_recent(
    args
):

    print_recent_papers(
        args.limit
    )

def handle_authors(
    args
):

    search_term = " ".join(
        args.search_term
    )


    search_and_print_authors(
        search_term,
        args.limit
    )

def handle_top(
    args
):

    print_top_cited_papers(
        args.limit
    )

def handle_collect(
    args
):

    search_term = " ".join(
        args.search_term
    )


    result = collect_papers(
        search_term
    )


    print(
        "Collection complete:"
    )


    print(
        f"Fetched: "
        f"{result['fetched']}"
    )


    print(
        f"Processed: "
        f"{result['processed']}"
    )


    print(
        f"Skipped: "
        f"{result['skipped']}"
    )


    print(
        f"Failed: "
        f"{result['failed']}"
    )

def handle_export(
    args
):

    connection = get_connection()


    try:

        if args.output:

            filename = args.output

        elif args.format == "csv":

            filename = "papers.csv"

        else:

            filename = "papers.json"


        if args.format == "csv":

            export_papers_to_csv(
                connection,
                filename
            )

        else:

            export_papers_to_json(
                connection,
                filename
            )


        print(
            f"Exported papers to {filename}"
        )


    finally:

        connection.close()

def create_parser():

    parser = argparse.ArgumentParser(
        description=(
            "Research paper collection "
            "and search application"
        )
    )


    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )


    collect_parser = subparsers.add_parser(
        "collect",
        help=(
            "Collect papers from OpenAlex"
        )
    )


    collect_parser.add_argument(
        "search_term",
        nargs="+",
        help=(
            "Search term used to collect papers"
        )
    )


    search_parser = subparsers.add_parser(
        "search",
        help=(
            "Search collected papers"
        )
    )


    search_parser.add_argument(
        "search_term",
        nargs="+",
        help=(
            "Search term"
        )
    )


    search_parser.add_argument(
        "--limit",
        type=positive_integer,
        default=DEFAULT_SEARCH_LIMIT,
        help=(
            "Maximum number of results"
        )
    )


    search_parser.add_argument(
        "--sort",
        choices=[
            "citations",
            "date",
            "title"
        ],
        default="citations",
        help=(
            "Sort results"
        )
    )
    
    stats_parser = subparsers.add_parser(
    "stats",
    help=(
        "Show database statistics"
       )
    )

    recent_parser = subparsers.add_parser(
    "recent",
    help="Show recently collected papers"
    )

    recent_parser.add_argument(
    "--limit",
    type=positive_integer,
    default=DEFAULT_SEARCH_LIMIT,
    help="Maximum number of papers to display"
    )

    authors_parser = subparsers.add_parser(
        "author",
        help=(
            "Collect authors from OpenAlex"
        )
    )

    authors_parser.add_argument(
    "--limit",
    type=positive_integer,
    default=DEFAULT_SEARCH_LIMIT,
    help="Maximum number of authors to display"
    )

    authors_parser.add_argument(
        "search_term",
        nargs="+",
        help=(
            "Search term used to collect authors"
        )
    )

    top_parser = subparsers.add_parser(
        "top",
        help="Show the most-cited papers"
    )

    top_parser.add_argument(
        "--limit",
        type=positive_integer,
        default=DEFAULT_SEARCH_LIMIT,
        help=(
            "Maximum number of papers "
            "to display"
        )
    )

    export_parser = subparsers.add_parser(
        "export",
        help="Export collected papers"
    )

    export_parser.add_argument(
        "--format",
        choices=[
            "csv",
            "json"
        ],
        required=True,
        help="Export format"
    )

    export_parser.add_argument(
        "--output",
        default=None,
        help="Output filename"
    )

    return parser

def main():

    parser = create_parser()


    args = parser.parse_args()


    if args.command == "collect":

        handle_collect(
            args
        )


    elif args.command == "search":

        handle_search(
            args
        )


    elif args.command == "stats":

        handle_stats()


    elif args.command == "recent":

        handle_recent(
            args
        )


    elif args.command == "author":

        handle_authors(
            args
        )


    elif args.command == "top":

        handle_top(
            args
        )


    elif args.command == "export":

        handle_export(
            args
        )

if __name__ == "__main__":

    main()