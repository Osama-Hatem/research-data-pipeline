from processing.normalizer import normalize_paper


def test_normalize_paper():

    paper = {
        "id": "W123",
        "title": "A Research Paper",
        "publication_date": "2025-01-01",
        "cited_by_count": 42,
        "authorships": [
            {
                "author": {
                    "id": "A123",
                    "display_name": "Ada Lovelace"
                }
            }
        ]
    }


    result = normalize_paper(
        paper,
        "engineering"
    )


    assert result["openalex_id"] == "W123"

    assert result["title"] == "A Research Paper"

    assert result["citations"] == 42

    assert result["search_query"] == "engineering"

    assert len(result["authors"]) == 1

    assert (
        result["authors"][0]["name"]
        == "Ada Lovelace"
    )

def test_normalize_paper_with_missing_data():

    paper = {
        "id": "W999",
        "title": "Incomplete Paper"
    }

    result = normalize_paper(
        paper,
        "engineering"
    )

    assert result["openalex_id"] == "W999"

    assert result["title"] == "Incomplete Paper"

    assert result["citations"] == 0

    assert result["authors"] == []