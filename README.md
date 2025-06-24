# Spotify API Automation Project

This project is a Python-based automation framework using Pytest for testing the Spotify Web API.  
It covers endpoints such as User Profile, Playlists, Tracks, Artists, Shows, Episodes, Markets, Player, and Search.

## Structure

- `tests/` – contains all API test cases
- `utils/` – helper modules for reusable code
- `data/` – test data in JSON format
- `conftest.py` – setup/teardown fixtures
- `requirements.txt` – dependencies

## Run Tests

```bash
pip install -r requirements.txt
pytest
```