import socket
import threading
from pathlib import Path

from response import Response
from router import Router

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080

# directory where static file are stored
STATIC_DIR = Path(__file__).resolve().parent / "static"

MIME_TYPES = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".txt": "text/plain",
    ".json": "application/json",
    ".ico": "image/x-icon",
    ".svg": "image/svg+xml",
}


def get_mime_type(file_path):
    # Extract the file extension from the path.
    ext = Path(file_path).suffix.lower()
    # Look up the extension in our MIME_TYPES dict.
    # If it's not found (e.g., .xyz), use "application/octet-stream"

    return MIME_TYPES.get(ext, "application/octet-stream")


def serve_static(request):
    # 1. Clean the path
    # Note: If path is just "/static", handling might vary, but this safely strips prefixes
    relative_path = request["path"].lstrip("/").removeprefix("static/").lstrip("/")

    # 2. Resolve paths completely to handle symlinks and relative dots (../)
    real_static_dir = STATIC_DIR.resolve()
    # Using joinpath safely combines them before resolution
    real_file_path = real_static_dir.joinpath(relative_path).resolve()

    # 3. Prevent Path Traversal
    if not real_file_path.is_relative_to(real_static_dir):
        return Response(
            status_code=403,
            headers={"Content-Type": "text/plain"},
            body="403 - Forbidden: Access denied",
        )

    # 4. Check existence AND ensure it's a file (not a directory)
    # Use real_file_path exclusively from this point onwards
    if not real_file_path.is_file():
        return Response(
            status_code=404,
            headers={"Content-Type": "text/plain"},
            body="404 - File not found",
        )

    # 5. Read and Serve (Always use the validated real_file_path)
    # Note: Consider a streaming response here if your framework supports it
    with open(real_file_path, "rb") as f:
        file_content = f.read()

    content_type = get_mime_type(real_file_path)

    return Response(
        status_code=200,
        headers={"Content-Type": content_type},
        body=file_content,
    )


def home_handler(request):
    return Response(
        status_code=200,
        headers={"Content-Type": "text/plain"},
        body="welcome to the home page!",
    )


def teapot_handler(request):
    return Response(
        status_code=418, headers={"Content-Type": "text/plain"}, body="I'm a teapot"
    )


def data_handler(request):
    return Response(
        status_code=200,
        headers={"Content-Type": "text/plain"},
        body="This is the data endpoint. Try sending a POST request here!",
    )


def not_found_handler(request):
    return Response(
        status_code=404,
        headers={"Content-Type": "text/plain"},
        body="404 - Page not found",
    )


def bad_request_handler(request):
    return Response(
        status_code=400, headers={"Content-Type": "text/plain"}, body="Bad Request"
    )


def parse_request(raw_data):
    # Guard agains't empty data
    if not raw_data:
        return None

    try:
        text = raw_data.decode("utf-8", errors="replace")
    except Exception:
        return None

    lines = text.split("\r\n")

    if not lines:
        return None

    request_line = lines[0]
    parts = request_line.split(" ")

    if len(parts) != 3:
        return None

    method, path, version = parts

    # parse headers
    headers = {}

    for line in lines[1:]:
        if line == "":
            break

        header_parts = line.split(": ", 1)

        if len(header_parts) != 2:
            continue

        key, value = header_parts
        headers[key] = value

    return {"method": method, "path": path, "version": version, "headers": headers}


def handle_client(client_socket, client_address):
    try:
        print(f"[NEW CONNECTION] {client_address} connected")

        request_data = client_socket.recv(4096)
        parsed = parse_request(request_data)

        if parsed is None:
            response = bad_request_handler(parsed)
            client_socket.sendall(response.serialize())  # ← removed .encode("utf-8")
            print(f"[{client_address}] sent 400 Bad Request")
            return

        # Route static file requests to serve_static()
        if parsed["path"].startswith("/static/"):  # ← new
            response = serve_static(parsed)  # ← new
        else:  # ← new
            handler = router.match(parsed["method"], parsed["path"])

            if handler is None:
                handler = not_found_handler

            response = handler(parsed)

        client_socket.sendall(response.serialize())  # ← removed .encode("utf-8")

        print(
            f"[{client_address}] {parsed['method']} {parsed['path']} → {response.status_code}"
        )

    except Exception as e:
        print(f"[ERROR] {client_address}: {e}")

    finally:
        client_socket.close()
        print(f"[DISCONNECTED] {client_address}")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on http://{SERVER_HOST}:{SERVER_PORT}")

    # create a router
    global router
    router = Router()
    router.add("GET", "/", home_handler)
    router.add("POST", "/data", data_handler)
    router.add("GET", "/tea", teapot_handler)

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            # spawn a new daemon thread for the client
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True,
            )

            thread.start()
            print(f"[ACTIVE THREADS] {threading.active_count()}")

    except KeyboardInterrupt:
        print("\nShutting down server...")

    finally:
        server_socket.close()
        print("Server socket closed.")


if __name__ == "__main__":
    start_server()
