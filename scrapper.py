import sys
import logging

from api.openalex import get_papers
from processing.normalizer import normalize_paper
from database.connection import get_connection
from database.schema import create_tables
from database.repository import save_paper
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


    processed_count = 0
    skipped_count = 0
    failed_count = 0


    for raw_paper in raw_papers:

        try:

            normalized_paper = normalize_paper(
                raw_paper,
                search_term
            )


            if not normalized_paper["openalex_id"]:

                logger.warning(
                    "Skipping paper with missing OpenAlex ID"
                )

                skipped_count += 1

                continue


            save_paper(
                normalized_paper,
                connection
            )


            processed_count += 1


        except Exception:

            failed_count += 1

            logger.exception(
                "Failed to process a paper"
            )

            continue


    connection.close()


    logger.info(
    "Collection complete: "
    "fetched=%d processed=%d skipped=%d failed=%d",
    len(raw_papers),
    processed_count,
    skipped_count,
    failed_count
    )


if __name__ == "__main__":

    main()