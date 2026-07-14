from collections import deque

def bfs(graph: dict[str, list[int]], start: str) -> list[str]:
    queue = deque([start])
    visited = {start}
    traversal = []

    while queue:
        node = queue.popleft()
        traversal.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append(node)
                visited.add(node)

    return traversal