from typing import List
from collections import deque

class TaskScheduler:
    def find_order(self, num_tasks: int, dependencies: List[List[int]]) -> List[int]:
        # 1. Initialize our data structures
        # graph maps: prerequisite -> list of dependent tasks
        graph = {i: [] for i in range(num_tasks)}
        in_degree = [0] * num_tasks

        # 2. Build the graph layout
        # Remember: pair [a, b] means to complete task 'a', you must first finish 'b' (b -> a)
        for dest, src in dependencies:
            graph[src].append(dest)
            in_degree[dest] += 1

        # 3. Collect all entry-point tasks (no dependencies remaining)
        queue = deque([i for i in range(num_tasks) if in_degree[i] == 0])
        execution_order = []

        # 4. Process the queue (The Domino Effect)
        while queue:
            current_task = queue.popleft()
            execution_order.append(current_task)

            for downstream_task in graph[current_task]:
                in_degree[downstream_task] -= 1

                if in_degree[downstream_task] == 0:
                    queue.append(downstream_task)

        # 5. cycle detection check 
        if len(execution_order) == num_tasks:
            return execution_order

        return []

