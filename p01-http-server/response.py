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

    def serialize(self):
        reason = self.REASON_PHRASES.get(self.status_code, "Unknown")

        status_line = f"HTTP/1.1 {self.status_code} {reason}"

        body_bytes = self.body.encode("utf-8")

        self.headers["Content-Length"] = str(len(body_bytes))

        headers_str = ""
        for key, value in self.headers.items():
            headers_str += f"{key}: {value}\r\n"

        response = f"{status_line}\r\n{headers_str}\r\n{self.body}"

        return response
