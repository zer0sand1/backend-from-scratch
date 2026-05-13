import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080


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
    # create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # set SO_REUSEADDR
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to HOST:PORT
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    # Listen
    server_socket.listen(1)
    print(f"Server listening on http://{SERVER_HOST}:{SERVER_PORT}")

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
                response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\nContent-Length: 11\r\n\r\nBad Request"
                client_socket.sendall(response.encode("utf-8"))
                client_socket.close()
                print("Sent 400 Bad Request\n")
                continue

            # print the parsed request line
            print(f"Method: {parsed['method']}")
            print(f"Path:   {parsed['path']}")
            print(f"Version:{parsed['version']}")

            # Print the parsed headers
            print("Headers:")
            for key, value in parsed["headers"].items():
                print(f" {key}: {value}")

            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 34\r\n\r\nHello from my custom HTTP server!"
            client_socket.sendall(response.encode("utf-8"))

            client_socket.close()
            print("Connection closed\n")

    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()
        print("Server socket closed.")


if __name__ == "__main__":
    start_server()
