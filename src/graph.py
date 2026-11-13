from fetcher import fetch_npm_dependencies


def get_package_deps(package_name, version, config, test_repo):
    """Возвращает прямые зависимости из тестового файла или сети."""
    if config["test_mode"]:
        return test_repo.get(package_name, {})
    clean_ver = version.lstrip("^~>=<")
    return fetch_npm_dependencies(config["repo_url"], package_name, clean_ver)


def build_dfs_graph(package_name, version, config, test_repo, path=None):
    """Строит граф зависимостей методом обхода в глубину с защитой от циклов."""
    if path is None:
        path = set()

    if package_name in path:
        return {"_cycle": True}

    new_path = path | {package_name}
    deps = get_package_deps(package_name, version, config, test_repo)
    subtree = {}

    for dep_name, dep_ver in deps.items():
        subtree[dep_name] = build_dfs_graph(
            dep_name, dep_ver, config, test_repo, new_path
        )

    return subtree


def print_graph(graph, indent=0):
    """Красиво выводит построенное дерево зависимостей на экран."""
    prefix = "  " * indent
    for pkg, sub_deps in graph.items():
        if isinstance(sub_deps, dict) and sub_deps.get("_cycle"):
            print(f"{prefix}- {pkg} [циклическая зависимость]")
        else:
            print(f"{prefix}- {pkg}")
            if isinstance(sub_deps, dict) and sub_deps:
                print_graph(sub_deps, indent + 1)
