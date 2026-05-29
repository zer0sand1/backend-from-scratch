import os
import tempfile
import shutil
from pathlib import Path

from server import serve_static, STATIC_DIR


def test_serve_static_html_file():
    # Request the existing index.html file
    request = {"method": "GET", "path": "/static/index.html", "version": "HTTP/1.1", "headers": {}}

    response = serve_static(request)

    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]
    # Body should contain some HTML content
    assert b"html" in response._body_bytes or b"HTML" in response._body_bytes


def test_serve_static_css_file():
    request = {"method": "GET", "path": "/static/style.css", "version": "HTTP/1.1", "headers": {}}

    response = serve_static(request)

    assert response.status_code == 200
    assert "text/css" in response.headers["Content-Type"]


def test_serve_static_nonexistent_file():
    # Request a file that doesn't exist
    request = {"method": "GET", "path": "/static/nonexistent.txt", "version": "HTTP/1.1", "headers": {}}

    response = serve_static(request)

    assert response.status_code == 404


def test_serve_static_path_traversal_attack():
    # Attempt to escape the static directory using ../
    # This should return 403 Forbidden, not the system file
    request = {"method": "GET", "path": "/static/../../../etc/passwd", "version": "HTTP/1.1", "headers": {}}

    response = serve_static(request)

    # Should be forbidden (403) or not found (404) — either way,
    # it must NOT return 200 with the contents of /etc/passwd
    assert response.status_code in (403, 404)


def test_serve_static_with_temp_file():
    # Create a temporary file in the static directory,
    # request it, then clean up.
    temp_file_path = Path(STATIC_DIR) / "test_temp_file.txt"
    try:
        # Write a temp file
        temp_file_path.write_text("temporary test content")

        request = {"method": "GET", "path": "/static/test_temp_file.txt", "version": "HTTP/1.1", "headers": {}}

        response = serve_static(request)

        assert response.status_code == 200
        assert "text/plain" in response.headers["Content-Type"]
        assert b"temporary test content" in response._body_bytes
    finally:
        # Always clean up the temp file, even if the test fails
        if temp_file_path.exists():
            temp_file_path.unlink()


def test_serve_static_directory_request():
    # Requesting /static/ (a directory, not a file) should return 404
    request = {"method": "GET", "path": "/static/", "version": "HTTP/1.1", "headers": {}}

    response = serve_static(request)

    # Requesting a directory, not a file — should be 404
    assert response.status_code == 404