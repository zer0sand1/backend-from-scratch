from server import get_mime_type


def test_mime_type_html():
    assert get_mime_type("index.html") == "text/html"


def test_mime_type_css():
    assert get_mime_type("style.css") == "text/css"


def test_mime_type_js():
    assert get_mime_type("script.js") == "application/javascript"


def test_mime_type_png():
    assert get_mime_type("photo.png") == "image/png"


def test_mime_type_jpg():
    assert get_mime_type("photo.jpg") == "image/jpeg"


def test_mime_type_jpeg():
    assert get_mime_type("photo.jpeg") == "image/jpeg"


def test_mime_type_json():
    assert get_mime_type("data.json") == "application/json"


def test_mime_type_svg():
    assert get_mime_type("icon.svg") == "image/svg+xml"


def test_mime_type_unknown_extension():
    # Unknown extensions should fall back to application/octet-stream
    assert get_mime_type("file.xyz") == "application/octet-stream"


def test_mime_type_no_extension():
    # A file with no extension should fall back to application/octet-stream
    assert get_mime_type("README") == "application/octet-stream"


def test_mime_type_case_insensitive():
    # Extensions should be case-insensitive: .CSS and .css should both work
    assert get_mime_type("style.CSS") == "text/css"
    assert get_mime_type("photo.PNG") == "image/png"
    assert get_mime_type("script.Js") == "application/javascript"


def test_mime_type_path_with_directory():
    # get_mime_type should work with full paths, not just filenames
    # Path.suffix extracts just the extension from any path
    assert get_mime_type("/static/css/style.css") == "text/css"
    assert get_mime_type("/static/js/app.js") == "application/javascript"