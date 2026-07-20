# Research Paper Collector

A Python research paper collection and search application that collects academic papers from OpenAlex, normalizes and stores the data in SQLite, supports structured search, author lookup, statistics, and exports results to CSV and JSON.

The project was built with a focus on clean architecture, testability, database design, and reliable data processing.

---

## Features

* Collect research papers from the OpenAlex API
* Search papers by:

  * Title
  * Author
  * Search query
* Search authors independently
* Sort papers by:

  * Citation count
  * Publication date
  * Title
* View:

  * Database statistics
  * Recently collected papers
  * Most-cited papers
* Export collected papers to:

  * CSV
  * JSON
* Store papers and authors using a relational SQLite database
* Prevent duplicate papers and authors
* Track author-paper relationships and author positions
* Handle incomplete or malformed paper data without stopping the entire collection process
* Validate CLI input
* Comprehensive automated testing with pytest

---

## Architecture

The application is organized into separate layers:

```text
CLI
 │
 ▼
Application Handlers
 │
 ├── Collection Service
 │    ├── OpenAlex API
 │    ├── Normalization
 │    └── Database Repository
 │
 ├── Search Services
 │    └── Database Reader
 │
 └── Export Services
      ├── CSV
      └── JSON
```

### Project Structure

```text
project/
│
├── api/
│   └── openalex.py
│
├── collection/
│   └── service.py
│
├── config/
│   ├── logging_config.py
│   └── settings.py
│
├── database/
│   ├── connection.py
│   ├── exporter.py
│   ├── reader.py
│   ├── repository.py
│   └── schema.py
│
├── processing/
│   └── normalizer.py
│
├── tests/
│   ├── test_app.py
│   ├── test_database.py
│   ├── test_openalex.py
│   └── ...
│
├── app.py
├── reader.py
├── scrapper.py
├── requirements.txt
└── README.md
```

---

## Database Design

The application uses SQLite with three main tables.

### Papers

Stores collected research papers.

```text
papers
├── id
├── openalex_id
├── title
├── publication_date
├── citations
├── doi
├── primary_url
├── search_query
└── collected_at
```

### Authors

Stores unique authors.

```text
authors
├── id
├── openalex_id
└── name
```

### Paper-Author Relationship

The many-to-many relationship between papers and authors is stored in:

```text
paper_authors
├── paper_id
├── author_id
└── author_position
```

This allows the application to:

* Associate multiple authors with one paper
* Associate one author with multiple papers
* Preserve author order

The database also uses unique constraints and indexes to improve data integrity and search performance.

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

The application is controlled through a command-line interface.

### Collect Papers

```bash
python app.py collect engineering
```

Multiple-word searches are supported:

```bash
python app.py collect machine learning
```

The collection pipeline:

```text
Search Term
    ↓
OpenAlex API
    ↓
Raw Paper Data
    ↓
Normalization
    ↓
Validation
    ↓
SQLite Database
```

Each paper is processed independently. If one paper fails, the remaining papers continue processing.

Example output:

```text
Collection complete:
Fetched: 25
Processed: 20
Skipped: 3
Failed: 2
```

---

### Search Papers

```bash
python app.py search engineering
```

Limit results:

```bash
python app.py search engineering --limit 5
```

Sort results:

```bash
python app.py search engineering --sort citations
```

Available sorting options:

```text
citations
date
title
```

Example:

```bash
python app.py search machine learning --sort date --limit 10
```

---

### View Statistics

```bash
python app.py stats
```

Displays database-level statistics such as:

* Total papers
* Total authors
* Total relationships
* Citation information

---

### View Recent Papers

```bash
python app.py recent
```

Limit the number of results:

```bash
python app.py recent --limit 5
```

---

### Search Authors

```bash
python app.py authors lovelace
```

Multiple-word searches are supported:

```bash
python app.py authors machine learning
```

Limit results:

```bash
python app.py authors smith --limit 10
```

---

### View Most-Cited Papers

```bash
python app.py top
```

Limit results:

```bash
python app.py top --limit 10
```

---

### Export Data

Export to CSV:

```bash
python app.py export --format csv
```

This creates:

```text
papers.csv
```

Specify a custom filename:

```bash
python app.py export \
    --format csv \
    --output research_papers.csv
```

Export to JSON:

```bash
python app.py export --format json
```

Specify a custom filename:

```bash
python app.py export \
    --format json \
    --output research_papers.json
```

---

## Testing

The project uses `pytest`.

Run the full test suite:

```bash
python -m pytest
```

The test suite covers:

* OpenAlex API behavior
* HTTP errors
* Retry behavior
* Paper normalization
* Database schema creation
* Paper insertion
* Duplicate prevention
* Author relationships
* Search functionality
* Sorting
* Statistics
* CLI argument parsing
* CLI command routing
* CSV export
* JSON export
* Invalid CLI input
* Temporary database testing

Tests use:

* In-memory SQLite databases
* `monkeypatch` for replacing external dependencies
* `tmp_path` for temporary export files
* Pytest fixtures for reusable test setup

The project avoids making real API requests during tests, making the test suite deterministic and fast.

---

## Engineering Decisions

### Layered Architecture

The project separates responsibilities between:

* API communication
* Data processing
* Database access
* Application logic
* CLI presentation

This makes the code easier to test and maintain.

---

### Database Normalization

Authors are stored separately from papers rather than duplicating author information inside every paper record.

This prevents:

* Duplicate author records
* Inconsistent author data
* Difficult author searches

The many-to-many relationship is handled through a junction table.

---

### Duplicate Prevention

Papers and authors use unique OpenAlex identifiers.

This allows the application to safely run the same collection command multiple times without duplicating existing records.

---

### Fault-Tolerant Collection

Each paper is processed independently.

A malformed paper does not stop the entire collection:

```text
Paper 1 → Processed
Paper 2 → Processed
Paper 3 → Failed
Paper 4 → Processed
Paper 5 → Skipped
```

The final collection summary reports:

```text
Fetched
Processed
Skipped
Failed
```

---

### Testable External Dependencies

External APIs and database connections are isolated so they can be replaced during testing.

For example, tests can replace:

```python
get_connection()
```

with an in-memory SQLite database.

This allows the application to be tested without depending on:

* A production database
* The OpenAlex API
* Existing local data
* External network availability

---

## Technology Stack

* Python
* SQLite
* Requests
* Pytest
* OpenAlex API
* argparse
* logging
* CSV
* JSON

---

## Future Improvements

Potential future improvements include:

* Pagination for larger OpenAlex result sets
* Configurable API request limits
* Additional export formats
* Full-text search using SQLite FTS5
* A web interface
* Background scheduled collection
* Database migrations
* Docker support
* CI/CD with GitHub Actions
* More advanced paper filtering
* Citation analytics
* Author profile pages
* Visualization of author collaboration networks

---

## What This Project Demonstrates

This project demonstrates practical backend engineering skills, including:

* Consuming a third-party REST API
* Designing a relational database
* Implementing a many-to-many relationship
* Building a command-line application
* Separating application responsibilities into layers
* Handling unreliable external data
* Writing automated tests
* Mocking external dependencies
* Testing CLI behavior
* Working with temporary files and databases
* Implementing CSV and JSON data export
* Designing fault-tolerant processing pipelines

---

## License

This project is available for educational and portfolio purposes.
