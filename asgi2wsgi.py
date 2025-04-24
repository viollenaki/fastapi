import asyncio
import io
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

# Копия библиотеки asgi2wsgi от Sebastian Ramirez (tiangolo)
class Asgi2Wsgi:
    def __init__(
        self, app: Callable, raise_exceptions: bool = False, workers: int = 10
    ):
        self.asgi_app = app
        self.raise_exceptions = raise_exceptions
        self.workers = workers

    def __call__(
        self, environ: Dict, start_response: Callable
    ) -> Union[List[bytes], Callable]:
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        future = asyncio.ensure_future(self.run_asgi(environ, start_response))
        return event_loop.run_until_complete(future)

    async def run_asgi(
        self, environ: Dict, start_response: Callable
    ) -> Union[List[bytes], Callable]:
        body = None
        if environ.get("wsgi.input"):
            body = environ["wsgi.input"].read()
        connections = {"scope": {}, "request": {}, "response": {"status": 0}}

        def set_path_info():
            path_info = environ["PATH_INFO"]
            connections["scope"]["path"] = path_info

        def set_root_path():
            script_name = environ.get("SCRIPT_NAME", "")
            if script_name:
                connections["scope"]["root_path"] = script_name

        def set_method():
            connections["scope"]["method"] = environ["REQUEST_METHOD"]

        def set_headers():
            connections["scope"]["headers"] = []
            for key, value in environ.items():
                if key.startswith("HTTP_"):
                    header = key[5:].lower().replace("_", "-").encode("latin1")
                    connections["scope"]["headers"].append(
                        (header, str(value).encode("latin1"))
                    )
                if key == "CONTENT_TYPE":
                    connections["scope"]["headers"].append(
                        (b"content-type", str(value).encode("latin1"))
                    )
                if key == "CONTENT_LENGTH":
                    connections["scope"]["headers"].append(
                        (b"content-length", str(value).encode("latin1"))
                    )

        def set_http_version():
            connections["scope"]["http_version"] = environ.get("SERVER_PROTOCOL", "HTTP/1.0").split(
                "/"
            )[1]

        def set_scheme():
            connections["scope"]["scheme"] = environ.get("wsgi.url_scheme", "http")

        def set_client():
            addr = environ.get("REMOTE_ADDR", None)
            port = environ.get("REMOTE_PORT", None)
            if addr:
                connections["scope"]["client"] = (addr, int(port) if port else None)

        def set_server():
            server = environ.get("SERVER_NAME", None)
            port = environ.get("SERVER_PORT", None)
            if server:
                connections["scope"]["server"] = (server, int(port) if port else None)

        async def receive():
            return {"type": "http.request", "body": body, "more_body": False}

        async def send(event):
            if event.get("type") == "http.response.start":
                status = event.get("status")
                connections["response"]["status"] = status

                headers = []
                for header_key, header_value in event.get("headers", []):
                    headers.append(
                        (
                            header_key.decode("latin1"),
                            header_value.decode("latin1"),
                        )
                    )

                start_response(f"{status} OK", headers)

            elif event.get("type") == "http.response.body":
                return [event.get("body", b"")]

        connections["scope"]["type"] = "http"

        set_path_info()
        set_root_path()
        set_method()
        set_headers()
        set_http_version()
        set_scheme()
        set_client()
        set_server()

        try:
            instance = self.asgi_app(connections["scope"])
            return await instance(receive, send)
        except Exception as e:
            if self.raise_exceptions:
                raise e from None
            output = io.StringIO()
            print("\nError:", file=output)
            print(e, file=output)
            print("\nASGI Scope:", file=output)
            for key, value in connections["scope"].items():
                print(f"{key}: {value}", file=output)
            print("\nHeaders:", file=output)
            for key_value in connections["scope"]["headers"]:
                print(key_value, file=output)
            print("\nWSGI Environ:", file=output)
            for key, value in environ.items():
                print(f"{key}: {value}", file=output)
            msg = output.getvalue()
            print(msg, file=sys.stderr)
            start_response("500 Internal Server Error", [("Content-Type", "text/plain")])
            return [str(e).encode()]
