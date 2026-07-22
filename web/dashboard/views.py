from django.http import FileResponse
from django.shortcuts import render, redirect

from database.connection import get_connection
from database.reader import (
    search_papers,
    search_authors,
    get_authors_for_paper,
)
from database.exporter import (
    export_papers_to_csv,
    export_papers_to_json,
)
from scrapper import collect_papers


def get_statistics(connection):

    paper_count = connection.execute(
        "SELECT COUNT(*) FROM papers"
    ).fetchone()[0]

    author_count = connection.execute(
        "SELECT COUNT(*) FROM authors"
    ).fetchone()[0]

    citation_count = connection.execute(
        """
        SELECT COALESCE(SUM(citations), 0)
        FROM papers
        """
    ).fetchone()[0]

    return {
        "paper_count": paper_count,
        "author_count": author_count,
        "citation_count": citation_count,
    }


def home(request):

    connection = get_connection()

    try:

        statistics = get_statistics(connection)

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

    limit = request.GET.get(
        "limit",
        "10",
    )

    sort_by = request.GET.get(
        "sort",
        "citations",
    )

    papers = []

    if search_term:

        try:

            limit = int(limit)

            if limit <= 0:
                limit = 10

        except ValueError:

            limit = 10

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

    if request.method == "POST":

        search_term = request.POST.get(
            "search_term",
            "",
        ).strip()

        if search_term:

            result = collect_papers(
                search_term
            )

    return render(
        request,
        "dashboard/collect.html",
        {
            "result": result,
            "search_term": search_term,
        },
    )


def statistics(request):

    connection = get_connection()

    try:

        stats = get_statistics(
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

    limit = request.GET.get(
        "limit",
        "10",
    )

    try:

        limit = int(limit)

        if limit <= 0:
            limit = 10

    except ValueError:

        limit = 10

    connection = get_connection()

    try:

        papers = connection.execute(
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
            ORDER BY collected_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

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

    limit = request.GET.get(
        "limit",
        "10",
    )

    try:

        limit = int(limit)

        if limit <= 0:
            limit = 10

    except ValueError:

        limit = 10

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

    limit = request.GET.get(
        "limit",
        "10",
    )

    try:

        limit = int(limit)

        if limit <= 0:
            limit = 10

    except ValueError:

        limit = 10

    connection = get_connection()

    try:

        papers = connection.execute(
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
            ORDER BY citations DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

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

        if not filename.endswith(".json"):
            filename += ".json"

    else:

        export_format = "csv"

        if not filename:
            filename = "papers.csv"

        if not filename.endswith(".csv"):
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

    response = FileResponse(
        open(filename, "rb"),
        as_attachment=True,
        filename=filename,
    )

    return response


def paper_detail(request, paper_id):

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
            (paper_id,),
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
