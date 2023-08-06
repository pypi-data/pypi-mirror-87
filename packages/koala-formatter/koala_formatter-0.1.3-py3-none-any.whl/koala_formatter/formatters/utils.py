from urllib3.util import parse_url


def get_host(host_url: str) -> str:
    if host_url:
        return parse_url(host_url).host
