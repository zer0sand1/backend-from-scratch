import socket
import threading
import time

import pytest

from server import (
    parse_request,
    handle_client,
    home_handler,
    data_handler,
    not_found_handler,
    bad_request_handler,
    serve_static,
)
from router import Router
from response import Response

TEST_PORT = 8085


def make_request(method, path, host="127.0.0.1", port=TEST_PORT, headers=None, body=""):
    """Send a raw HTTP request and return the full response as bytes."""
    request_line = f"{method} {path} HTTP/1.1\r\n"
    host_header = f"Host: {host}\r\n"

    extra_headers = ""
    if headers:
        for key, value in headers.items():
            extra_headers += f"{key}: {value}\r\n"

    content_length_header = ""
    if body:
        content_length_header = f"Content-Length: {len(body)}\r\n"

    request = request_line + host_header + content_length_header + extra_headers + "\r\n" + body

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((host, port))
    sock.sendall(request.encode("utf-8"))

    response = sock.recv(4096)
    sock.close()

    return response


def parse_response(raw_response):
    """Parse a raw HTTP response into status line, headers dict, and body."""
    decoded = raw_response.decode("utf-8", errors="replace")
    parts = decoded.split("\r\n\r\n", 1)

    header_section = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    header_lines = header_section.split("\r\n")
    status_line = header_lines[0]

    headers = {}
    for line in header_lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value

    return {
        "status_line": status_line,
        "headers": headers,
        "body": body,
    }


@pytest.fixture(scope="module")
def server_fixture():
    """Start the HTTP server in a background thread for all tests in this module."""
    from server import STATIC_DIR

    router = Router()
    router.add("GET", "/", home_handler)
    router.add("POST", "/data", data_handler)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", TEST_PORT))
    server_socket.listen(5)

    def handle_test_client(client_socket, client_address):
        """Handle a client connection using the test router."""
        try:
            request_data = client_socket.recv(4096)
            parsed = parse_request(request_data)

            if parsed is None:
                response = bad_request_handler(parsed)
                client_socket.sendall(response.serialize())
                return

            if parsed["path"].startswith("/static/"):
                response = serve_static(parsed)
            else:
                handler = router.match(parsed["method"], parsed["path"])
                if handler is None:
                    handler = not_found_handler
                response = handler(parsed)

            client_socket.sendall(response.serialize())

        except Exception as e:
            print(f"[TEST ERROR] {client_address}: {e}")
        finally:
            client_socket.close()

    def accept_connections():
        try:
            while True:
                client_socket, client_address = server_socket.accept()
                thread = threading.Thread(
                    target=handle_test_client,
                    args=(client_socket, client_address),
                    daemon=True,
                )
                thread.start()
        except OSError:
            pass

    server_thread = threading.Thread(target=accept_connections, daemon=True)
    server_thread.start()

    # Give the server time to start listening
    time.sleep(0.1)

    yield  # Tests run here

    server_socket.close()


def test_get_home_page(server_fixture):
    response = make_request("GET", "/")
    parsed = parse_response(response)

    assert "200" in parsed["status_line"]
    assert "welcome to the home page!" in parsed["body"]


def test_post_data_endpoint(server_fixture):
    response = make_request("POST", "/data")
    parsed = parse_response(response)

    assert "200" in parsed["status_line"]


def test_404_unknown_route(server_fixture):
    response = make_request("GET", "/nonexistent")
    parsed = parse_response(response)

    assert "404" in parsed["status_line"]


def test_static_html_file(server_fixture):
    response = make_request("GET", "/static/index.html")
    parsed = parse_response(response)

    assert "200" in parsed["status_line"]
    assert "text/html" in parsed["headers"].get("Content-Type", "")


def test_static_css_file(server_fixture):
    response = make_request("GET", "/static/style.css")
    parsed = parse_response(response)

    assert "200" in parsed["status_line"]
    assert "text/css" in parsed["headers"].get("Content-Type", "")


def test_static_nonexistent_file(server_fixture):
    response = make_request("GET", "/static/nope.txt")
    parsed = parse_response(response)

    assert "404" in parsed["status_line"]


def test_content_length_header(server_fixture):
    response = make_request("GET", "/")
    parsed = parse_response(response)

    assert "Content-Length" in parsed["headers"]


def test_malformed_request(server_fixture):
    """Send a malformed request (only 2 parts in the request line)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect(("127.0.0.1", TEST_PORT))
    sock.sendall(b"GET /\r\n\r\n")

    response = sock.recv(4096)
    sock.close()

    decoded = response.decode("utf-8", errors="replace")
    assert "400" in decoded


def test_method_not_allowed(server_fixture):
    """POST to a GET-only route should return 404."""
    response = make_request("POST", "/")
    parsed = parse_response(response)

    assert "404" in parsed["status_line"]