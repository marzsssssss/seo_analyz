import requests
from bs4 import BeautifulSoup
import pytest

BASE_URLS = [
    "https://quickex.io",
    "https://swapgate.io"
]

@pytest.mark.parametrize("url", BASE_URLS)
def test_seo_tags(url):

    response = requests.get(url)

    assert response.status_code == 200, f"Ошибка сервера: код ответа {response.status_code}"

    x_robots_tag = response.headers.get("X-Robots-Tag", "").lower()
    assert "noindex" not in x_robots_tag, "X-Robots-Tag содержит 'noindex'"
    assert "nofollow" not in x_robots_tag, "X-Robots-Tag содержит 'nofollow'"

    soup = BeautifulSoup(response.text, 'html.parser')

    meta_robots = soup.find("meta", {"name": "robots"})
    if meta_robots:
        content = meta_robots.get("content", "").lower()
        assert "noindex" not in content, "<meta name='robots'> содержит 'noindex'"
        assert "nofollow" not in content, "<meta name='robots'> содержит 'nofollow'"


if __name__ == "__main__":
    pytest.main([__file__])
