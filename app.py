import argparse

from scrapper import collect_papers
from reader import search_and_print


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
        type=int,
        default=10,
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


    return parser


def main():

    parser = create_parser()


    args = parser.parse_args()


    search_term = " ".join(
        args.search_term
    )


    if args.command == "collect":

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


    elif args.command == "search":

        search_and_print(
            search_term,
            args.limit,
            args.sort
        )


if __name__ == "__main__":

    main()