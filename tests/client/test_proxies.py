import pytest

import httpx


@pytest.mark.parametrize(
    ["proxies", "expected_proxies"],
    [
        ("http://127.0.0.1", [("all", "http://127.0.0.1")]),
        ({"all": "http://127.0.0.1"}, [("all", "http://127.0.0.1")]),
        (
            {"http": "http://127.0.0.1", "https": "https://127.0.0.1"},
            [("http", "http://127.0.0.1"), ("https", "https://127.0.0.1")],
        ),
        (httpx.HTTPProxy("http://127.0.0.1"), [("all", "http://127.0.0.1")]),
        (
            {"https": httpx.HTTPProxy("https://127.0.0.1"), "all": "http://127.0.0.1"},
            [("all", "http://127.0.0.1"), ("https", "https://127.0.0.1")],
        ),
    ],
)
def test_proxies_parameter(proxies, expected_proxies):
    client = httpx.Client(proxies=proxies)

    for proxy_key, url in expected_proxies:
        assert proxy_key in client.proxies
        assert client.proxies[proxy_key].proxy_url == url

    assert len(expected_proxies) == len(client.proxies)


def test_proxies_has_same_properties_as_dispatch():
    client = httpx.AsyncClient(proxies="http://127.0.0.1")
    pool = client.dispatch
    proxy = client.proxies["all"]

    assert isinstance(pool, httpx.ConnectionPool)
    assert isinstance(proxy, httpx.HTTPProxy)

    for prop in [
        "verify",
        "cert",
        "timeout",
        "pool_limits",
        "http_versions",
        "backend",
    ]:
        assert getattr(pool, prop) == getattr(proxy, prop)
