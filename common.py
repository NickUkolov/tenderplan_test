from requests.adapters import HTTPAdapter, Retry
from requests import Response, Session
from fake_headers import Headers


def requests_get(url: str) -> Response:
    with Session() as session:
        headers = Headers(headers=True).generate()
        retries = Retry(
            total=5,
            backoff_factor=1,
            method_whitelist=["GET"],
            status_forcelist=[404, 502, 503, 504],
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session.get(url, headers=headers)
