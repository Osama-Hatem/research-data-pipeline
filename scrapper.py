import sys
import logging

from api.openalex import get_papers
from database.connection import get_connection
from database.schema import create_tables
from collection.service import process_papers
from config.logging_config import configure_logging


configure_logging()


logger = logging.getLogger(__name__)


def main():

    if len(sys.argv) < 2:

        logger.error(
            "Usage: python scrapper.py <search term>"
        )

        return


    search_term = sys.argv[1]


    logger.info(
        "Starting collection for '%s'",
        search_term
    )


    connection = get_connection()


    try:

        create_tables(
            connection
        )


        raw_papers = get_papers(
            search_term
        )


        logger.info(
            "Fetched %d papers",
            len(raw_papers)
        )


        (
            processed_count,
            skipped_count,
            failed_count
        ) = process_papers(
            raw_papers,
            search_term,
            connection
        )


        logger.info(
            "Collection complete: "
            "fetched=%d processed=%d skipped=%d failed=%d",
            len(raw_papers),
            processed_count,
            skipped_count,
            failed_count
        )


    finally:

        connection.close()


if __name__ == "__main__":

    main()