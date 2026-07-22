from django.http import FileResponse
from django.shortcuts import render

from database.connection import get_connection
from database.reader import (
    search_papers,
    search_authors,
    get_authors_for_paper,
    get_database_statistics,
    get_recent_papers,
    get_top_cited_papers,
)
from database.exporter import (
    export_papers_to_csv,
    export_papers_to_json,
)
from scrapper import collect_papers


def parse_positive_integer(
    value,
    default=10,
):
    try:
        value = int(value)

        if value <= 0:
            return default

        return value

    except (TypeError, ValueError):

        return default


def home(request):

    connection = get_connection()

    try:

        statistics = get_database_statistics(
            connection
        )

        return render(
            request,
            "dashboard/home.html",
            {
                "statistics": statistics,
            },
        )

    finally:

        connection.close()


def search(request):

    search_term = request.GET.get(
        "q",
        "",
    ).strip()

    limit = parse_positive_integer(
        request.GET.get(
            "limit",
            "10",
        )
    )

    sort_by = request.GET.get(
        "sort",
        "citations",
    )

    papers = []

    if search_term:

        connection = get_connection()

        try:

            papers = search_papers(
                connection,
                search_term,
                limit,
                sort_by,
            )

        finally:

            connection.close()

    return render(
        request,
        "dashboard/search.html",
        {
            "search_term": search_term,
            "papers": papers,
            "limit": limit,
            "sort_by": sort_by,
        },
    )


def collect(request):

    result = None
    search_term = ""
    limit = 25
    target_new = ""

    error = None

    if request.method == "POST":

        search_term = request.POST.get(
            "search_term",
            "",
        ).strip()

        limit = parse_positive_integer(
            request.POST.get(
                "limit",
                "25",
            ),
            default=25,
        )

        target_new = request.POST.get(
            "new",
            "",
        ).strip()

        if target_new:

            target_new = parse_positive_integer(
                target_new,
                default=1,
            )

        else:

            target_new = None

        if not search_term:

            error = "Please enter a search term."

        else:

            try:

                result = collect_papers(
                    search_term,
                    limit=limit,
                    target_new=target_new,
                )

            except Exception as exception:

                error = str(
                    exception
                )

    return render(
        request,
        "dashboard/collect.html",
        {
            "result": result,
            "search_term": search_term,
            "limit": limit,
            "target_new": target_new,
            "error": error,
        },
    )


def statistics(request):

    connection = get_connection()

    try:

        stats = get_database_statistics(
            connection
        )

        return render(
            request,
            "dashboard/statistics.html",
            {
                "statistics": stats,
            },
        )

    finally:

        connection.close()


def recent(request):

    limit = parse_positive_integer(
        request.GET.get(
            "limit",
            "10",
        )
    )

    connection = get_connection()

    try:

        papers = get_recent_papers(
            connection,
            limit,
        )

        return render(
            request,
            "dashboard/recent.html",
            {
                "papers": papers,
                "limit": limit,
            },
        )

    finally:

        connection.close()


def authors(request):

    search_term = request.GET.get(
        "q",
        "",
    ).strip()

    limit = parse_positive_integer(
        request.GET.get(
            "limit",
            "10",
        )
    )

    results = []

    if search_term:

        connection = get_connection()

        try:

            results = search_authors(
                connection,
                search_term,
                limit,
            )

        finally:

            connection.close()

    return render(
        request,
        "dashboard/authors.html",
        {
            "search_term": search_term,
            "authors": results,
            "limit": limit,
        },
    )


def top(request):

    limit = parse_positive_integer(
        request.GET.get(
            "limit",
            "10",
        )
    )

    connection = get_connection()

    try:

        papers = get_top_cited_papers(
            connection,
            limit,
        )

        return render(
            request,
            "dashboard/top.html",
            {
                "papers": papers,
                "limit": limit,
            },
        )

    finally:

        connection.close()


def export_data(request):

    if request.method != "POST":

        return render(
            request,
            "dashboard/export.html",
        )

    export_format = request.POST.get(
        "format",
        "csv",
    )

    filename = request.POST.get(
        "filename",
        "",
    ).strip()

    if export_format == "json":

        if not filename:

            filename = "papers.json"

        if not filename.endswith(
            ".json"
        ):

            filename += ".json"

    else:

        export_format = "csv"

        if not filename:

            filename = "papers.csv"

        if not filename.endswith(
            ".csv"
        ):

            filename += ".csv"

    connection = get_connection()

    try:

        if export_format == "json":

            export_papers_to_json(
                connection,
                filename,
            )

        else:

            export_papers_to_csv(
                connection,
                filename,
            )

    finally:

        connection.close()

    return FileResponse(
        open(
            filename,
            "rb",
        ),
        as_attachment=True,
        filename=filename,
    )


def paper_detail(
    request,
    paper_id,
):

    connection = get_connection()

    try:

        paper = connection.execute(
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
            WHERE id = ?
            """,
            (
                paper_id,
            ),
        ).fetchone()

        if paper is None:

            return render(
                request,
                "dashboard/paper_detail.html",
                {
                    "paper": None,
                    "authors": [],
                },
                status=404,
            )

        authors = get_authors_for_paper(
            connection,
            paper_id,
        )

        return render(
            request,
            "dashboard/paper_detail.html",
            {
                "paper": paper,
                "authors": authors,
            },
        )

    finally:

        connection.close()
