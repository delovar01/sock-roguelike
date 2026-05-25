"""A* поиск пути на тайловой сетке.

Дейкстра ищет пути ко всем вершинам — расточительно, если нужна одна цель.
A* добавляет эвристику h (манхэттен) и сразу идёт в сторону цели.
Приоритет вершины: f = g + h.
"""

import heapq


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# 4 направления — без диагоналей
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_path(level, start, goal):
    """Возвращает путь от start до goal (без start). Если пути нет — []."""
    if start == goal:
        return []
    if not level.is_walkable(goal[0], goal[1]):
        return []

    open_heap = [(0, start)]
    came_from = {start: None}
    g_score = {start: 0}

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal:
            # восстанавливаем путь
            path = []
            while came_from[current] is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        cx, cy = current
        for dx, dy in DIRS:
            nx, ny = cx + dx, cy + dy
            if not level.is_walkable(nx, ny):
                continue
            tentative = g_score[current] + 1
            if tentative < g_score.get((nx, ny), 10 ** 9):
                came_from[(nx, ny)] = current
                g_score[(nx, ny)] = tentative
                f = tentative + manhattan((nx, ny), goal)
                heapq.heappush(open_heap, (f, (nx, ny)))

    return []
