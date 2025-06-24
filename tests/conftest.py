from datetime import datetime

import pytest

@pytest.fixture(scope="session")
def auth_headers():
    token = "Bearer BQD_QUtcqyTYILYKE9HJfznpyhOchTJBI7jk96hn-zrnLR5dMssSB1R2celWP3S8hU2rUkQ_dWY5p2ixivBGmjvk3Ew0D8qgm0KfIpRu7Lr54MX-cIX0MieaTGgPde1I6CSjoOEGHKrK-EbzECCtxWHt6ihu1y43X-B1AmPVs6hhGCd-qAtiNhOQlAUCqoGvJ8wXjTkcT-ZVIsccbYmzxt8_YoJGQz9hLqrmamx7rJbwFPMvTqksCwmpuC3caoiq4cJ7m1PFXqO_9HZPaVC6iOFEBuXNSscK0GjUp4NvQIGZ6PZjOFC7PW6RJstGdUbf0zlC4wT21MQuXjw-kkhd71c8UieCjzcOd64WAUIzJCGiIjCOnepQ0V_raFIY"
    return {
        "Authorization": token,
        "Content-Type": "application/json"
    }

@pytest.fixture(scope="session")
def base_url():
    return "https://api.spotify.com/v1"

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Add timestamp to report file name
    report_dir = "reports"
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = f"{report_dir}/report_{now}.html"

@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    print("\nSetting up resources...")
    yield
    print("\nTearing down resources...")