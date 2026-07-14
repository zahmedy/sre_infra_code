from collections import deque

def bfs(graph: dict[str, list[str]], start: str) -> list[str]:
    queue = deque([start])
    visited = {start}
    traversal = []

    while queue:
        node = queue.popleft()
        traversal.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return traversal

def bfs_all(graph: dict[str, list[str]], start: str) -> list[str]:
    visited = set()
    traversal = []

    for start in graph:
        if start in visited:
            continue

        queue = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            traversal.append(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)

    return traversal