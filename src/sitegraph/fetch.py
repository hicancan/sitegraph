from __future__ import annotations

import threading

import requests
from dataclasses import dataclass
from urllib.parse import urljoin

DEFAULT_HEADERS = {
    'User-Agent': 'sitegraph/0.1 (+https://github.com/hicancan/sitegraph)'
}

_local = threading.local()


def _session() -> requests.Session:
    """One keep-alive session per thread, so consecutive requests to a site reuse the connection."""
    session = getattr(_local, "session", None)
    if session is None:
        session = _local.session = requests.Session()
        session.headers.update(DEFAULT_HEADERS)
    return session


@dataclass
class FetchResult:
    url: str
    final_url: str
    status_code: int | None
    text: str
    error: str | None = None


@dataclass
class RedirectResult:
    url: str
    status_code: int | None
    location: str | None
    error: str | None = None


def fetch_html(url: str, timeout: int = 20, verify: bool = True) -> FetchResult:
    try:
        resp = _session().get(url, timeout=timeout, verify=verify)
        resp.encoding = resp.apparent_encoding or resp.encoding
        return FetchResult(url=url, final_url=str(resp.url), status_code=resp.status_code, text=resp.text)
    except Exception as exc:
        return FetchResult(url=url, final_url=url, status_code=None, text='', error=str(exc))


def fetch_redirect_location(url: str, timeout: int = 20, verify: bool = True) -> RedirectResult:
    try:
        resp = _session().get(url, timeout=timeout, verify=verify, allow_redirects=False)
        location = resp.headers.get('Location')
        if location:
            location = urljoin(str(resp.url), location)
        return RedirectResult(url=url, status_code=resp.status_code, location=location)
    except Exception as exc:
        return RedirectResult(url=url, status_code=None, location=None, error=str(exc))
