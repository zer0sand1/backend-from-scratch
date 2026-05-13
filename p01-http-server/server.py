import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080


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

            request_data = client_socket.recv(4096)
            print(f"Received {len(request_data)} bytes")
            print("--- Raw Request ---")
            print(request_data.decode("utf-8", errors="replace"))

            response = response = (
                "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 34\r\n\r\nHello from my custom HTTP server!"
            )
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
