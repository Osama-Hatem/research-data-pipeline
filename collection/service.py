import logging

from processing.normalizer import normalize_paper
from database.repository import save_paper


logger = logging.getLogger(__name__)


def process_papers(
    raw_papers,
    search_term,
    connection
):

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


    return (
        processed_count,
        skipped_count,
        failed_count
    )