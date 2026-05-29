from response import Response


def test_serialize_basic_200_response():
    # A simple 200 OK response with a text body
    response = Response(
        status_code=200,
        headers={"Content-Type": "text/plain"},
        body="Hello!",
    )

    result = response.serialize()

    # The result should be bytes
    assert isinstance(result, bytes)

    # The result should contain the status line
    assert b"HTTP/1.1 200 OK" in result

    # The result should contain the Content-Type header
    assert b"Content-Type: text/plain" in result

    # The result should contain the body
    assert b"Hello!" in result


def test_serialize_404_response():
    # A 404 Not Found response
    response = Response(
        status_code=404,
        headers={"Content-Type": "text/plain"},
        body="Page not found",
    )

    result = response.serialize()

    assert b"HTTP/1.1 404 Not Found" in result
    assert b"Page not found" in result


def test_serialize_bytes_body():
    # When body is bytes (e.g., an image file),
    # serialize should handle it without crashing.
    # This tests the isinstance(body, bytes) branch in __init__.
    binary_data = b"\x89PNG\r\n\x1a\n"  # PNG file header bytes
    response = Response(
        status_code=200,
        headers={"Content-Type": "image/png"},
        body=binary_data,
    )

    result = response.serialize()

    assert isinstance(result, bytes)
    assert b"HTTP/1.1 200 OK" in result
    assert binary_data in result


def test_serialize_empty_body():
    # What happens with an empty body?
    response = Response(
        status_code=204,
        headers={},
        body="",
    )

    result = response.serialize()

    # Content-Length should be 0
    assert b"Content-Length: 0" in result

    # The response should still have a valid status line
    assert b"HTTP/1.1 204 No Content" in result


def test_serialize_multibyte_characters():
    # Characters like é, 中, 🎉 take more than 1 byte in UTF-8.
    # Content-Length must be in BYTES, not characters.
    # "Héllo" is 6 bytes: H(1) + é(2) + l(1) + l(1) + o(1) = 6
    response = Response(
        status_code=200,
        headers={"Content-Type": "text/plain; charset=utf-8"},
        body="Héllo",
    )

    result = response.serialize()

    # Content-Length should be 6 (bytes), NOT 5 (characters)
    assert b"Content-Length: 6" in result

    # The body should still be present and correct
    assert "Héllo".encode("utf-8") in result


def test_serialize_multiple_headers():
    # A response with multiple custom headers
    response = Response(
        status_code=200,
        headers={
            "Content-Type": "text/html",
            "X-Custom-Header": "hello",
            "Server": "MyHTTPServer/1.0",
        },
        body="<h1>Hi</h1>",
    )

    result = response.serialize()

    assert b"Content-Type: text/html" in result
    assert b"X-Custom-Header: hello" in result
    assert b"Server: MyHTTPServer/1.0" in result
    assert b"<h1>Hi</h1>" in result


def test_serialize_unknown_status_code():
    # What if someone uses a status code not in REASON_PHRASES?
    # It should fall back to "Unknown".
    response = Response(
        status_code=999,
        headers={"Content-Type": "text/plain"},
        body="Weird status",
    )

    result = response.serialize()

    # Should use "Unknown" as the reason phrase
    assert b"HTTP/1.1 999 Unknown" in result


def test_serialize_content_length_auto_calculated():
    # Content-Length should be automatically calculated from the body,
    # NOT manually set by the user.
    response = Response(
        status_code=200,
        headers={"Content-Type": "text/plain"},
        body="Hello",
    )

    result = response.serialize()

    # "Hello" is 5 bytes
    assert b"Content-Length: 5" in result
