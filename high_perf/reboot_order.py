from collections import deque

def reboot_order(
    dependencies: dict[str, list[str]]
) -> list[list[str]]:
    indegree = {
        service: len(deps)
        for service, deps in dependencies.items()
    }
    
    dependents = {
        service: []
        for service in dependencies
    }

    # reverse adjacency 
    for service, deps in dependencies.items():
        for dep in deps:
            dependents[dep].append(service)

    queue = deque(
        service
        for service, degree in indegree.items()
        if degree == 0
    )

    execution_groups = []
    processed = 0

    # process each task in queue and append released ones
    while queue:
        group = []

        for _ in range(len(queue)):
            service = queue.popleft()
            group.append(service)
            processed += 1

            for dependent in dependents[service]:
                indegree[dependent] -= 1

                if indegree[dependent] == 0:
                    queue.append(dependent)

        execution_groups.append(group)

    if processed != len(dependencies):
        raise ValueError("dependency cycle detected")

    return execution_groups