# Research Data Collection Pipeline

A Python-based research paper collection and analysis system.

## Current Features

- OpenAlex API integration
- Research paper normalization
- SQLite database storage
- Author-paper relationships
- Duplicate prevention
- Automated testing with pytest

## Architecture

OpenAlex API
↓
API Client
↓
Data Normalizer
↓
Repository Layer
↓
SQLite Database

## Testing

Run:

```bash
python -m pytest