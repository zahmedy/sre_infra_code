from collections import deque

def reboot_order(
    dependencies: dict[str, list[str]]
) -> list[str]:
    execution_order = []

    dependents = {} 
    indegree = {}

    queue = deque()

    for service in dependencies:
        indegree[service] = len(dependencies[service])
        # add zero dependencies tasks to queue
        if indegree[service] == 0:
            queue.append(service)
        
        dependents[service] = []

    for service, deps in dependencies.items():
        for dep in deps:
            dependents[dep].append(service)

    while queue:
        first_service = queue.popleft()
        execution_order.append(first_service)

        freed_services = dependents[first_service]

        for service in freed_services:
            indegree[service] -= 1
            if indegree[service] == 0:
                queue.append(service)

    if len(execution_order) != len(dependencies):
        raise ValueError("dependency cycle detected")

    return execution_order