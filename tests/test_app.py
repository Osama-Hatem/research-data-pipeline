import json
import app
import pytest
from app import create_parser, handle_export
from database.connection import get_connection
from database.schema import create_tables
from database.repository import save_paper
from argparse import Namespace


@pytest.fixture
def database_connection():

    connection = get_connection(
        ":memory:"
    )


    create_tables(
        connection
    )


    paper = {

        "openalex_id": "W123",

        "title": "Test Research Paper",

        "publication_date": "2025-01-01",

        "citations": 42,

        "doi": None,

        "primary_url": None,

        "search_query": "engineering",

        "authors": []

    }


    save_paper(
        paper,
        connection
    )


    yield connection


    connection.close()
    

def test_collect_command_calls_collect_papers(
        monkeypatch
    ):

        received = {}


        def fake_collect_papers(
            search_term,
            limit,
            target_new=None
        ):

            received[
                "search_term"
            ] = search_term


            received[
                "limit"
            ] = limit


            received[
                "target_new"
            ] = target_new


            return {

                "fetched": 10,

                "new": 8,

                "existing": 1,

                "skipped": 1,

                "failed": 0,

                "pages": 1

            }


        monkeypatch.setattr(
            app,
            "collect_papers",
            fake_collect_papers
        )


        monkeypatch.setattr(
            "sys.argv",
            [
                "app.py",
                "collect",
                "machine",
                "learning",
                "--limit",
                "25"
            ]
        )


        app.main()


        assert received[
            "search_term"
        ] == "machine learning"


        assert received[
            "limit"
        ] == 25


        assert received[
            "target_new"
        ] is None
        
def test_search_command_calls_search_and_print(
    monkeypatch
):

    received = {}


    def fake_search_and_print(
        search_term,
        limit,
        sort_by
    ):

        received[
            "search_term"
        ] = search_term


        received[
            "limit"
        ] = limit


        received[
            "sort_by"
        ] = sort_by


    monkeypatch.setattr(
        app,
        "search_and_print",
        fake_search_and_print
    )


    monkeypatch.setattr(
        "sys.argv",
        [
            "app.py",
            "search",
            "machine",
            "learning",
            "--limit",
            "5",
            "--sort",
            "title"
        ]
    )


    app.main()


    assert received[
        "search_term"
    ] == "machine learning"


    assert received[
        "limit"
    ] == 5


    assert received[
        "sort_by"
    ] == "title"

def test_collect_command_prints_summary(
    monkeypatch,
    capsys
):

    def fake_collect_papers(
        search_term,
        limit,
        target_new=None
    ):

        return {

            "fetched": 25,

            "new": 20,

            "existing": 0,

            "skipped": 3,

            "failed": 2,

            "pages": 1

        }


    monkeypatch.setattr(
        app,
        "collect_papers",
        fake_collect_papers
    )


    monkeypatch.setattr(
        "sys.argv",
        [
            "app.py",
            "collect",
            "engineering"
        ]
    )


    app.main()


    output = capsys.readouterr().out


    assert (
        "Fetched: 25"
        in output
    )


    assert (
        "New: 20"
        in output
    )


    assert (
        "Already existed: 0"
        in output
    )


    assert (
        "Skipped: 3"
        in output
    )


    assert (
        "Failed: 2"
        in output
    )
    
def test_export_parser_accepts_csv():

    parser = create_parser()


    args = parser.parse_args(
        [
            "export",
            "--format",
            "csv"
        ]
    )


    assert args.command == "export"

    assert args.format == "csv"

    assert args.output is None


def test_export_parser_accepts_custom_output():

    parser = create_parser()


    args = parser.parse_args(
        [
            "export",
            "--format",
            "csv",
            "--output",
            "research.csv"
        ]
    )


    assert args.command == "export"

    assert args.format == "csv"

    assert args.output == "research.csv"


def test_handle_export_csv(
    monkeypatch,
    tmp_path,
    database_connection
):

    paper = {

        "openalex_id": "W123",

        "title": "Test Research Paper",

        "publication_date": "2025-01-01",

        "citations": 42,

        "doi": None,

        "primary_url": None,

        "search_query": "engineering",

        "authors": []

    }

    output_file = (
        tmp_path
        / "papers.csv"
    )


    args = Namespace(

        format="csv",

        output=str(
            output_file
        )

    )


    monkeypatch.setattr(
        "app.get_connection",
        lambda: database_connection 
    )


    handle_export(
        args
    )


    assert output_file.exists()


    content = (
        output_file.read_text(
            encoding="utf-8"
        )
    )


    assert (
        "Test Research Paper"
        in content
    )

def test_handle_export_json(
    monkeypatch,
    tmp_path,
    database_connection
):

    output_file = (
        tmp_path
        / "papers.json"
    )


    args = Namespace(

        format="json",

        output=str(
            output_file
        )

    )


    monkeypatch.setattr(
        "app.get_connection",
        lambda: database_connection
    )


    handle_export(
        args
    )


    assert output_file.exists()


    content = (
        output_file.read_text(
            encoding="utf-8"
        )
    )


    exported_papers = json.loads(
        content
    )


    assert len(
        exported_papers
    ) == 1


    assert (
        exported_papers[0]["title"]
        == "Test Research Paper"
    )


    assert (
        exported_papers[0]["openalex_id"]
        == "W123"
    )

def test_stats_command_calls_print_statistics(
    monkeypatch,
):
    called = {
        "value": False,
    }

    def fake_print_statistics():
        called["value"] = True

    monkeypatch.setattr(
        app,
        "print_statistics",
        fake_print_statistics,
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "app.py",
            "stats",
        ],
    )

    app.main()

    assert called["value"] is True

def test_recent_command_calls_print_recent_papers(
    monkeypatch,
):
    received = {}

    def fake_print_recent_papers(limit):
        received["limit"] = limit

    monkeypatch.setattr(
        app,
        "print_recent_papers",
        fake_print_recent_papers,
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "app.py",
            "recent",
            "--limit",
            "5",
        ],
    )

    app.main()

    assert received["limit"] == 5

def test_authors_command_calls_handle_authors(
    monkeypatch,
):
    received = {}

    def fake_handle_authors(args):
        received["args"] = args

    monkeypatch.setattr(
        app,
        "handle_authors",
        fake_handle_authors,
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "app.py",
            "author",
            "machine",
            "learning",
            "--limit",
            "7",
        ],
    )

    app.main()

    args = received["args"]

    assert args.command == "author"

    assert (
        args.search_term
        == [
            "machine",
            "learning",
        ]
    )

    assert args.limit == 7

def test_top_command_calls_print_top_cited_papers(
    monkeypatch,
):
    received = {}

    def fake_print_top_cited_papers(limit):
        received["limit"] = limit

    monkeypatch.setattr(
        app,
        "print_top_cited_papers",
        fake_print_top_cited_papers,
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "app.py",
            "top",
            "--limit",
            "3",
        ],
    )

    app.main()

    assert received["limit"] == 3

def test_limit_must_be_positive():

    parser = create_parser()


    try:

        parser.parse_args(
            [
                "recent",
                "--limit",
                "0",
            ]
        )

    except SystemExit as error:

        assert error.code == 2

    else:

        raise AssertionError(
            "Expected parser to reject zero limit"
        )
    
def test_negative_limit_is_rejected():

    parser = create_parser()


    try:

        parser.parse_args(
            [
                "top",
                "--limit",
                "-5",
            ]
        )

    except SystemExit as error:

        assert error.code == 2

    else:

        raise AssertionError(
            "Expected parser to reject negative limit"
        )
    
def test_export_requires_format():

    parser = create_parser()


    try:

        parser.parse_args(
            [
                "export",
            ]
        )

    except SystemExit as error:

        assert error.code == 2

    else:

        raise AssertionError(
            "Expected export format to be required"
        )

def test_export_rejects_invalid_format():

    parser = create_parser()


    try:

        parser.parse_args(
            [
                "export",
                "--format",
                "xml",
            ]
        )

    except SystemExit as error:

        assert error.code == 2

    else:

        raise AssertionError(
            "Expected invalid export format to be rejected"
        )
    
def test_handle_export_closes_connection_when_export_fails(
    monkeypatch,
):
    closed = {
        "value": False,
    }


    class FakeConnection:

        def close(self):

            closed["value"] = True


    def fake_get_connection():

        return FakeConnection()


    def fake_export_papers_to_csv(
        connection,
        filename,
    ):

        raise RuntimeError(
            "Export failed"
        )


    monkeypatch.setattr(
        app,
        "get_connection",
        fake_get_connection,
    )


    monkeypatch.setattr(
        app,
        "export_papers_to_csv",
        fake_export_papers_to_csv,
    )


    args = Namespace(

        format="csv",

        output="papers.csv",

    )


    try:

        app.handle_export(
            args
        )

    except RuntimeError as error:

        assert str(
            error
        ) == "Export failed"

    else:

        raise AssertionError(
            "Expected export to fail"
        )


    assert closed["value"] is True