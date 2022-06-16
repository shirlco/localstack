from localstack.runtime.hooks import on_infra_ready as on_ready
from localstack.runtime.hooks import on_infra_start as on_start

__all__ = [
    "on_ready",
    "on_start",
]
