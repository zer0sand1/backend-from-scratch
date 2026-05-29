from server import parse_request


def test_parse_get_request():
    # Arrange
    raw_data = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"

    # Act
    result = parse_request(raw_data)

    # Assert
    assert result is not None, "parse_request should return a dict, not None"
    assert result["method"] == "GET"
    assert result["path"] == "/"
    assert result["version"] == "HTTP/1.1"
    assert result["headers"]["Host"] == "localhost"


def test_parse_post_request():
    raw_data = b"POST /data HTTP/1.1\r\nContent-Length: 10\r\nHost: localhost\r\n\r\n"

    result = parse_request(raw_data)

    assert result is not None
    assert result["method"] == "POST"
    assert result["path"] == "/data"
    assert result["headers"]["Content-Length"] == "10"


def test_parse_multiple_headers():
    # A request with multiple headers
    raw_data = b"GET / HTTP/1.1\r\nHost: localhost\r\nAccept: */*\r\nUser-Agent: curl/8.0\r\n\r\n"

    result = parse_request(raw_data)

    assert result is not None
    assert result["headers"]["Host"] == "localhost"
    assert result["headers"]["Accept"] == "*/*"
    assert result["headers"]["User-Agent"] == "curl/8.0"


def test_parse_empty_data():
    # Empty bytes should return None (malformed request)
    raw_data = b""

    result = parse_request(raw_data)

    assert result is None


def test_parse_malformed_request_line():
    # A request line with only 2 parts (missing HTTP version) should return None
    raw_data = b"GET /\r\n\r\n"

    result = parse_request(raw_data)

    assert result is None


def test_parse_path_with_query_params():
    # A URL with query parameters — path should include everything before the first space after method
    # Note: our parser doesn't separate query params — it includes them in the path.
    # This is expected behavior for now.
    raw_data = b"GET /search?q=hello HTTP/1.1\r\nHost: localhost\r\n\r\n"

    result = parse_request(raw_data)

    assert result is not None
    assert result["path"] == "/search?q=hello"
