class Response:
    REASON_PHRASES = {
        200: "OK",
        201: "Created",
        204: "No Content",
        301: "Moved Permanently",
        302: "Found",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
    }

    def __init__(self, status_code=200, headers=None, body=""):
        self.status_code = status_code
        self.headers = headers if headers is not None else {}
        self.body = body

        if isinstance(body, bytes):
            self._body_bytes = body
        else:
            self._body_bytes = body.encode("utf-8")

    def serialize(self):
        # the status line e.g "HTTP/1.1 200 OK
        reason = self.REASON_PHRASES.get(self.status_code, "Unknown")
        status_line = f"HTTP/1.1 {self.status_code} {reason}"

        # Content-Lenght is numbe of bytes in the body
        self.headers["Content-Length"] = str(len(self._body_bytes))

        # Build the headers section: "Key: Value\r\n" for each header
        headers_str = ""
        for key, value in self.headers.items():
            headers_str += f"{key}: {value}\r\n"

        # Combine status line + headers + blank line + body
        headers_part = f"{status_line}\r\n{headers_str}\r\n".encode("utf-8")

        return headers_part + self._body_bytes
