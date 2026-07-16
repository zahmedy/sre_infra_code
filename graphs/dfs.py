def has_cycle(graph: dict[str, list[str]]) -> bool:
    visited = set()
    path = set()

    def dfs(node) -> bool:
        visited.add(node)
        path.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in path:
                    return True
        
        path.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True

    return False