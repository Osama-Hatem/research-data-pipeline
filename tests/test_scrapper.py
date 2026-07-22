import collection.service

from collection.service import process_papers


def test_process_papers_continues_after_one_failure(
    monkeypatch
    ):

    raw_papers = [

        {
            "id": "paper-1"
        },

        {
            "id": "paper-2"
        },

        {
            "id": "paper-3"
        }

    ]


    def fake_normalize_paper(
        raw_paper,
        search_term
    ):

        if raw_paper[
            "id"
        ] == "paper-2":

            raise ValueError(
                "Intentional test failure"
            )


        return {

            "openalex_id": raw_paper[
                "id"
            ],

            "title": "Test Paper",

            "publication_date":
            "2025-01-01",

            "citations": 0,

            "doi": None,

            "primary_url": None,

            "search_query": search_term,

            "authors": []

        }


    def fake_save_paper(
        paper,
        connection
    ):

        return True


    monkeypatch.setattr(
        collection.service,
        "normalize_paper",
        fake_normalize_paper
    )


    monkeypatch.setattr(
        collection.service,
        "save_paper",
        fake_save_paper
    )


    result = process_papers(
        raw_papers,
        "engineering",
        None
    )


    assert result == {

        "new": 2,

        "existing": 0,

        "skipped": 0,

        "failed": 1

    }

def test_process_papers_skips_paper_without_openalex_id(
    monkeypatch
):

    raw_papers = [

        {
            "id": "paper-1"
        }

    ]


    def fake_normalize_paper(
        raw_paper,
        search_term
    ):

        return {

            "openalex_id": None,

            "title": "Paper Without ID",

            "publication_date":
            "2025-01-01",

            "citations": 0,

            "doi": None,

            "primary_url": None,

            "search_query": search_term,

            "authors": []

        }


    monkeypatch.setattr(
        collection.service,
        "normalize_paper",
        fake_normalize_paper
    )


    result = process_papers(
        raw_papers,
        "engineering",
        None
    )


    assert result == {

        "new": 0,

        "existing": 0,

        "skipped": 1,

        "failed": 0

    }