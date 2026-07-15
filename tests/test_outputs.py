import json
from pathlib import Path

REPORT = Path("/app/report.json")


def test_report_exists():
    """The agent produced a report file."""
    assert REPORT.exists(), "no report.json found"


def test_report_valid_json():
    """The report is valid JSON."""
    data = json.loads(REPORT.read_text())
    assert isinstance(data, dict), "report.json is not a JSON object"


def test_total_requests():
    """total_requests must be 6."""
    data = json.loads(REPORT.read_text())
    assert data.get("total_requests") == 6, f"expected 6, got {data.get('total_requests')}"


def test_unique_ips():
    """unique_ips must be 3."""
    data = json.loads(REPORT.read_text())
    assert data.get("unique_ips") == 3, f"expected 3, got {data.get('unique_ips')}"


def test_top_path():
    """top_path must be /index.html."""
    data = json.loads(REPORT.read_text())
    assert data.get("top_path") == "/index.html", f"expected /index.html, got {data.get('top_path')}"
