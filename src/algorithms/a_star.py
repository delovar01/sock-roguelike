"""A* поиск пути на тайловой сетке.

Дейкстра ищет пути ко всем вершинам — расточительно когда нужна одна цель.
A* добавляет эвристику h (манхэттенское расстояние) и идёт сразу в сторону
цели. Приоритет вершины f = g + h, где g — стоимость от старта,
h — оценка оставшегося пути.
"""

import heapq


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# 4 направления — без диагоналей
NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_path(level, start, goal):
    """Возвращает список тайлов от start до goal (не включая start).

    Если пути нет — пустой список.
    """
    if start == goal:
        return []
    # если цель в стене — пути нет
    if not level.is_walkable(*goal):
        return []

    open_heap = []
    heapq.heappush(open_heap, (0, start))
    came_from = {start: None}
    g_score = {start: 0}

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal:
            return _reconstruct(came_from, current)

        cx, cy = current
        for dx, dy in NEIGHBORS:
            nx, ny = cx + dx, cy + dy
            if not level.is_walkable(nx, ny):
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get((nx, ny), 10 ** 9):
                came_from[(nx, ny)] = current
                g_score[(nx, ny)] = tentative_g
                f = tentative_g + manhattan((nx, ny), goal)
                heapq.heappush(open_heap, (f, (nx, ny)))

    return []


def _reconstruct(came_from, current):
    path = []
    while came_from.get(current) is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
