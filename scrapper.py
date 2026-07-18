import sys

from api.openalex import get_papers
from processing.normalizer import normalize_paper
from database.repository import save_paper


def main():

    if len(sys.argv) < 2:

        print(
            "Usage: "
            "python scrapper.py <search term>"
        )

        return


    search_term = sys.argv[1]


    raw_papers = get_papers(
        search_term
    )


    for raw_paper in raw_papers:

        normalized_paper = normalize_paper(
            raw_paper,
            search_term
        )


        if not normalized_paper["openalex_id"]:

            continue


        save_paper(
            normalized_paper
        )


    print(
        f"Processed "
        f"{len(raw_papers)} papers"
    )


if __name__ == "__main__":

    main()