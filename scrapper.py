import sys
import logging

from api.openalex import get_papers
from database.connection import get_connection
from database.schema import create_tables
from collection.service import process_papers
from config.logging_config import configure_logging


configure_logging()


logger = logging.getLogger(
    __name__
)


def collect_papers(
    search_term,
    limit=25,
    target_new=None,
    max_pages=100
):

    connection = get_connection()


    try:

        create_tables(
            connection
        )


        total_fetched = 0

        total_new = 0

        total_existing = 0

        total_skipped = 0

        total_failed = 0

        page = 1


        while page <= max_pages:

            raw_papers = get_papers(
                search_term,
                limit,
                page
            )


            if not raw_papers:

                break


            total_fetched += len(
                raw_papers
            )


            result = process_papers(
                raw_papers,
                search_term,
                connection
            )


            total_new += result[
                "new"
            ]


            total_existing += result[
                "existing"
            ]


            total_skipped += result[
                "skipped"
            ]


            total_failed += result[
                "failed"
            ]


            if (

                target_new is not None

                and total_new >= target_new

            ):

                break


            if len(
                total_fetched
            ) < limit:

                break


            page += 1


        return {

            "fetched": total_fetched,

            "new": total_new,

            "existing": total_existing,

            "skipped": total_skipped,

            "failed": total_failed,

            "pages": page

        }


    finally:

        connection.close()

def main():

    if len(
        sys.argv
    ) < 2:

        logger.error(
            "Usage: "
            "python scrapper.py "
            "<search term>"
        )

        return


    search_term = " ".join(
        sys.argv[1:]
    )


    result = collect_papers(
        search_term
    )


    logger.info(
        "Collection complete: "
        "fetched=%d new=%d "
        "existing=%d skipped=%d "
        "failed=%d",

        result["fetched"],

        result["new"],

        result["existing"],

        result["skipped"],

        result["failed"]
    )


if __name__ == "__main__":

    main()