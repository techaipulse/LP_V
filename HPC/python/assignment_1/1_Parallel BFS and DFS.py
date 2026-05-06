# Title:Design and implement Parallel Breadth First Search and Depth First Search based on existing
# algorithms using OpenMP. Use a Tree or an undirected graph for BFS and DFS .

from concurrent.futures import ThreadPoolExecutor
from collections import deque

# ----------- CHOOSE MODE -----------
# 1 = User Input Graph
# 2 = Predefined Graph
mode = int(input("Enter 1 for Input Graph OR 2 for Default Graph: "))

# ----------- GRAPH CREATION -----------
if mode == 1:
    n = int(input("Enter number of nodes: "))
    e = int(input("Enter number of edges: "))

    graph = {i: [] for i in range(n)}

    print("Enter edges (u v):")
    for _ in range(e):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    start = int(input("Enter starting node: "))

else:
    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1, 5],
        5: [2, 4]
    }
    start = 0


# ------------------ PARALLEL BFS ------------------
def parallel_bfs(graph, start):
    visited = set([start])
    queue = deque([start])

    print("\nParallel BFS:")

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            current_level.append(queue.popleft())

        print(current_level, end=" ")

        def process(node):
            temp = []
            for nbr in graph[node]:
                if nbr not in visited:
                    visited.add(nbr)
                    temp.append(nbr)
            return temp

        next_nodes = []
        with ThreadPoolExecutor() as executor:
            results = executor.map(process, current_level)

        for res in results:
            next_nodes.extend(res)

        for n in next_nodes:
            queue.append(n)

    print()


# ------------------ PARALLEL DFS ------------------
def parallel_dfs(graph, node, visited):
    visited.add(node)
    print(node, end=" ")

    def task(nbr):
        if nbr not in visited:
            parallel_dfs(graph, nbr, visited)

    with ThreadPoolExecutor() as executor:
        futures = []
        for nbr in graph[node]:
            if nbr not in visited:
                futures.append(executor.submit(task, nbr))

        for f in futures:
            f.result()


# ------------------ RUN ------------------
parallel_bfs(graph, start)

print("\nParallel DFS:")
visited = set()
parallel_dfs(graph, start, visited)