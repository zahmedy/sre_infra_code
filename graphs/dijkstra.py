import heapq

def shortest_latency(graph, start, target):
    if not graph:
        return -1
    
    if start == target:
        return 0

    # Start dijkstra's algorthim from start node
    heap = [(0, start)]

    # Keep track of min current distance in distance HashMap
    distance = {
        node: float("inf")
        for node in graph
    }
    distance[start] = 0

    while heap:
        cost, node = heapq.heappop(heap)

        # If reached target it is guaranteed cost is the min latency
        if node == target:
            return cost

        # Explore all edges from node
        for neighbor, neighbor_cost in graph[node]:
            new_cost = neighbor_cost + cost

            # Is this route cheaper than current or skip
            if new_cost < distance[neighbor]:
                distance[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor))
            if new_cost > distance[neighbor]:
                continue

    return -1