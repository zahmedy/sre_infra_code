from collections import deque

def deployment_order(graph):
    reverse_adjacency = {
        service: []
        for service in graph
    }
    indegree = {
        service: 0
        for service in graph
    }

    for service in graph:
        for prerequisite in graph[service]:
            reverse_adjacency[prerequisite].append(service)
            indegree[service] += 1

    queue = deque(
        service
        for service in graph
        if indegree[service] == 0
    )

    execution_order = []

    while queue:
        current_service = queue.popleft()
        execution_order.append(current_service)

        for released_service in reverse_adjacency[current_service]:
            indegree[released_service] -= 1
            if indegree[released_service] == 0:
                queue.append(released_service)

    if len(execution_order) != len(graph):
        return -1

    return execution_order

graph = {
    "API": ["Auth", "Cache"],
    "Auth": ["DB"],
    "Cache": ["DB"],
    "DB": []
}

reverse = {
    "Auth": ["API"],
    "Cache": ["API"],
    "DB": ["Auth", "Cache"],
    "API": []
}