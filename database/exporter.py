import csv
import json

cols = [

        "id",

        "openalex_id",

        "title",

        "publication_date",

        "citations",

        "doi",

        "primary_url",

        "search_query",

        "collected_at"

    ]

def get_all_papers(
    connection
):

    return connection.execute(
        """
        SELECT
            id,
            openalex_id,
            title,
            publication_date,
            citations,
            doi,
            primary_url,
            search_query,
            collected_at
        FROM papers
        ORDER BY id
        """
    ).fetchall()


def export_papers_to_csv(
    connection,
    filename
):

    papers = get_all_papers(
        connection
    )


    columns = cols


    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )


        writer.writerow(
            columns
        )


        writer.writerows(
            papers
        )


def export_papers_to_json(
    connection,
    filename
):

    papers = get_all_papers(
        connection
    )


    columns = cols


    data = [

        dict(
            zip(
                columns,
                paper
            )
        )

        for paper in papers

    ]


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )