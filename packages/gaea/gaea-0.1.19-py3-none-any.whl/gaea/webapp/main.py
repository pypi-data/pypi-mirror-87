import fastapi
from fastapi.middleware.cors import CORSMiddleware


class AppClient:
    def __init__(self, routers, middleware=None):
        self.app = fastapi.FastAPI()

        if not isinstance(routers, (list, tuple)):
            routers = [routers]

        for router in routers:
            self.app.include_router(router)

        self.middleware = middleware

    def _add_middleware(self):
        if self.middleware:
            self.app.middleware("http")(self.middleware)

    def add_cors_middleware(
        self,
        allow_origins=None,
        allow_methods=None,
        allow_headers=None,
        allow_credentials=False,
    ):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins or ["*"],
            allow_methods=allow_methods or ["*"],
            allow_headers=allow_headers or ["*"],
            allow_credentials=allow_credentials,
        )

    def get_app(self):
        self._add_middleware()
        return self.app
