from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "search/",
        views.search,
        name="search",
    ),

    path(
        "collect/",
        views.collect,
        name="collect",
    ),

    path(
        "statistics/",
        views.statistics,
        name="statistics",
    ),

    path(
        "recent/",
        views.recent,
        name="recent",
    ),

    path(
        "authors/",
        views.authors,
        name="authors",
    ),

    path(
        "top/",
        views.top,
        name="top",
    ),

    path(
        "export/",
        views.export_data,
        name="export",
    ),

    path(
        "paper/<int:paper_id>/",
        views.paper_detail,
        name="paper_detail",
    ),

]
