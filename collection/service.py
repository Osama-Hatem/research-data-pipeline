import logging

from processing.normalizer import normalize_paper
from database.repository import save_paper


logger = logging.getLogger(
    __name__
)


def process_papers(
    raw_papers,
    search_term,
    connection
):

    new_count = 0

    existing_count = 0

    skipped_count = 0

    failed_count = 0


    for raw_paper in raw_papers:

        try:

            normalized_paper = normalize_paper(
                raw_paper,
                search_term
            )


            if not normalized_paper[
                "openalex_id"
            ]:

                logger.warning(
                    "Skipping paper with "
                    "missing OpenAlex ID"
                )


                skipped_count += 1

                continue


            was_inserted = save_paper(
                normalized_paper,
                connection
            )


            if was_inserted:

                new_count += 1

            else:

                existing_count += 1


        except Exception:

            failed_count += 1


            logger.exception(
                "Failed to process a paper"
            )


            continue


    return {

        "new": new_count,

        "existing": existing_count,

        "skipped": skipped_count,

        "failed": failed_count

    }