"""轻量反向代理：/api/ -> 后端 8000，其他 -> H5 静态文件"""
import os
import http.server
import urllib.request
import urllib.error

BACKEND = "http://localhost:8000"
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        if self.path.startswith("/api/"):
            self._proxy()
        elif self.path.startswith("/health"):
            self._proxy()
        else:
            # SPA: 非 /api 且无文件后缀的路径返回 index.html
            if "." not in self.path.split("?")[0].rsplit("/", 1)[-1]:
                self.path = "/index.html"
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            self._proxy()
        else:
            self.send_error(404)

    def do_PUT(self):
        if self.path.startswith("/api/"):
            self._proxy()
        else:
            self.send_error(404)

    def do_DELETE(self):
        if self.path.startswith("/api/"):
            self._proxy()
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def _proxy(self):
        target = f"{BACKEND}{self.path}"
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else None
        req = urllib.request.Request(target, data=body, method=self.command)
        # Copy headers
        for key, val in self.headers.items():
            if key.lower() not in ("host", "content-length"):
                req.add_header(key, val)
        try:
            with urllib.request.urlopen(req) as resp:
                self.send_response(resp.status)
                for key, val in resp.getheaders():
                    if key.lower() not in ("transfer-encoding",):
                        self.send_header(key, val)
                self._set_cors_headers()
                self.end_headers()
                data = resp.read()
                if data:
                    self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self._set_cors_headers()
            self.end_headers()
            if e.fp:
                self.wfile.write(e.fp.read())

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

    def end_headers(self):
        super().end_headers()


if __name__ == "__main__":
    port = 10086
    print(f"Proxy server running on http://0.0.0.0:{port}")
    print(f"  /api/* -> {BACKEND}")
    print(f"  /*     -> {STATIC_DIR}")
    server = http.server.HTTPServer(("0.0.0.0", port), ProxyHandler)
    server.serve_forever()
