import socket

from response import Response
from router import Router

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080


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


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print(f"Server listening on http://{SERVER_HOST}:{SERVER_PORT}")

    # create a router
    router = Router()
    router.add("GET", "/", home_handler)
    router.add("POST", "/data", data_handler)
    router.add("GET", "/tea", teapot_handler)
    try:
        while True:
            print("Waiting for a connection....")
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # parse request
            request_data = client_socket.recv(4096)
            parsed = parse_request(request_data)

            # if parsing fails
            if parsed is None:
                response = bad_request_handler(parsed)
                client_socket.sendall(response.serialize().encode("utf-8"))
                client_socket.close()
                print("Sent 400 Bad Request\n")
                continue

            handler = router.match(parsed["method"], parsed["path"])

            if handler is None:
                handler = not_found_handler

            response = handler(parsed)
            client_socket.sendall(response.serialize().encode("utf-8"))

            print(f"Method: {parsed['method']}")
            print(f"Path:   {parsed['path']}")
            print(f"Version: {parsed['version']}")

            # Print the parsed headers
            print("Headers:")
            for key, value in parsed["headers"].items():
                print(f" {key}: {value}")

            print(f"Handler: {handler.__name__}")
            print(f"Response status: {response.status_code}")
            print()

            client_socket.close()

    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()
        print("Server socket closed.")


if __name__ == "__main__":
    start_server()
