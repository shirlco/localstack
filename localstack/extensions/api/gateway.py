from localstack.aws.handlers import (
    serve_custom_service_request_handlers as custom_service_request_handlers,
)
from localstack.services.edge import ROUTER as custom_routes

__all__ = [
    "custom_service_request_handlers",
    "custom_routes",
]
