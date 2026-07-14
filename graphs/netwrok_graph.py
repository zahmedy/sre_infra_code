from collections import deque
import heapq

def shortest_recovery_path(
    grid: list[list[int]],
    start: tuple[int, int],
    target: tuple[int, int]
) -> int:
    if not grid or not grid[0]:
        return -1
    
    rows, cols = len(grid), len(grid[0])
    
    def is_valid_position(position: tuple[int, int]) -> bool:
        row, col = position
        return 0 <= row < rows and 0 <= col < cols
    
    if not is_valid_position(start) or not is_valid_position(target):
        return -1
    
    start_row, start_col = start
    target_row, target_col = target

    if grid[start_row][start_col] != 0:
        return -1
    
    if grid[target_row][target_col] != 0:
        return -1
    
    if start == target:
        return 0
    
    queue = deque([(start_row, start_col, 0)])
    visited = {start}

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    while queue:
        row, col, steps = queue.popleft()

        if (row, col) == target:
            return steps

        for n_row, n_col in directions:
            new_row = row+n_row
            new_col = col+n_col
            position = (new_row, new_col)
            if (
                is_valid_position(position) 
                and grid[new_row][new_col] == 0
                and position not in visited
            ):
                visited.add(position)
                queue.append((new_row, new_col ,steps+1))

    return -1


def minimum_network_latency(
    n: int,
    connections: list[list[int]],
    start: int,
    target: int
) -> int:
    """
    Using dijkstra's algorithm to find the shortest path(lowest latency in network)
    """
    
    adjancey_nodes = [[] for _ in range(n)]
    for source, distenation, latency in connections:
        adjancey_nodes[source].append((distenation, latency))

    distance = [float("inf")] * n
    distance[start] = 0

    heap = [(0, start)]

    while heap:
        current_distance, current_node = heapq.heappop(heap)
        
        if current_distance > distance[current_node]:
            continue

        if current_node == target:
            return current_distance

        for neighbor_node, weight in adjancey_nodes[current_node]:
            new_distance = current_distance + weight

            if new_distance < distance[neighbor_node]:
                distance[neighbor_node] = new_distance
                heapq.heappush(
                    heap, 
                    (new_distance, neighbor_node)
                )

    return -1

def connected_server_group(
        n: int,
        connections: list[list[int]]
) -> int:
    adjacency_list = [[] for _ in range(n)]

    for node, neighbor in connections:
        adjacency_list[node].append(neighbor)
        adjacency_list[neighbor].append(node)

    visited = set()
    group_counter = 0

    for server in range(n):
        if server in visited:
            continue

        group_counter += 1
        stack = [server]
        visited.add(server)

        while stack:
            current = stack.pop()

            for adj_server in adjacency_list[current]:
                if adj_server not in visited:
                    visited.add(adj_server)
                    stack.append(adj_server)

    return group_counter

from collections import deque

def has_dependency_cycle(
    n: int,
    dependencies: list[list[int]]
) -> bool:
    adjancey = [[] for _ in range(n)]
    indegree = [0] * n

    for service, prerequisite in dependencies:
        adjancey[prerequisite].append(service)
        indegree[service] += 1

    queue = deque(
        service
        for service in range(n)
        if indegree[service] == 0
    )

    services_done = 0

    while queue:
        current_service = queue.popleft()
        services_done += 1

        for service in adjancey[current_service]:
            indegree[service] -=1
            
            if indegree[service] == 0:
                queue.append(service)

    return services_done != n