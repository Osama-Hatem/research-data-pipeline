import sys
import logging

from api.openalex import get_papers
from database.connection import get_connection
from database.schema import create_tables
from collection.service import process_papers
from config.logging_config import configure_logging


configure_logging()


logger = logging.getLogger(__name__)


def collect_papers(
    search_term
):

    connection = get_connection()


    try:

        create_tables(
            connection
        )


        raw_papers = get_papers(
            search_term
        )


        result = process_papers(
            raw_papers,
            search_term,
            connection
        )


        return {

            "fetched": len(raw_papers),

            "processed": result[
                0
            ],

            "skipped": result[
                1
            ],

            "failed": result[
                2
            ]

        }


    finally:

        connection.close()


def main():

    if len(sys.argv) < 2:

        logger.error(
            "Usage: "
            "python scrapper.py <search term>"
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
        "fetched=%d processed=%d "
        "skipped=%d failed=%d",
        result["fetched"],
        result["processed"],
        result["skipped"],
        result["failed"]
    )


if __name__ == "__main__":

    main()