import json
import urllib.error
import urllib.request

REQUEST_TIMEOUT = 10


def fetch_npm_dependencies(repo_url, package_name, version):
    """Загружает прямые зависимости npm-пакета заданной версии по URL."""
    clean_url = repo_url.rstrip("/")
    target_url = f"{clean_url}/{package_name}/{version}"

    try:
        with urllib.request.urlopen(target_url, timeout=REQUEST_TIMEOUT) as resp:
            raw_data = resp.read().decode("utf-8")
            package_data = json.loads(raw_data)
    except urllib.error.HTTPError as err:
        raise ValueError(f"Пакет или версия не найдены (HTTP {err.code})")
    except urllib.error.URLError as err:
        raise ConnectionError(f"Ошибка сети при обращении к {target_url}: {err.reason}")

    return package_data.get("dependencies", {})
