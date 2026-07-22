# Django Frontend

This frontend provides a browser interface for the existing Research Paper Collector.

It does not replace the CLI.

## Features

The web interface mirrors the current CLI features:

- Search papers
- Collect papers from OpenAlex
- Database statistics
- Recently collected papers
- Search authors
- Top cited papers
- Export CSV
- Export JSON
- View paper details

## Run

From the project root:

```bash
pip install django
python web/manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Important

The frontend imports and uses the existing project modules:

```text
database/
scrapper.py
```

Therefore `web/manage.py` must add the project root to Python's import path.

The existing CLI remains unchanged.
