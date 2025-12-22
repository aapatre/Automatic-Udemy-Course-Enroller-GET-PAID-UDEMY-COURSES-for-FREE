from dataclasses import dataclass
from typing import Generic, Optional, TypeVar


T = TypeVar("T")
E = TypeVar("E")


class HttpRequestFailed(Exception):
    def __init__(self, url: str, status: Optional[int] = None, reason: Optional[str] = None, retryable: bool = False):
        self.url = url
        self.status = status
        self.reason = reason
        self.retryable = retryable
        super().__init__(f"HTTP request failed: {status} {reason} @ {url} (retryable={retryable})")


@dataclass
class Result(Generic[T, E]):
    ok: bool
    value: Optional[T] = None
    error: Optional[E] = None
