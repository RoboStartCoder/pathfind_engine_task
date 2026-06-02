import random
import time
from typing import List

from pathfind_engine.api.Executor import Player, CellStatus, MoveTo


class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Map:
    def __init__(self):
        self.player: Object = Object(0, 0)
        self.exit_pos: Object = Object(0, 0)
        self.walls: List[Object] = []

    def set_player(self, x: int, y: int):
        self.player = Object(x, y)

    def set_exit_pos(self, x: int, y: int):
        self.exit_pos = Object(x, y)


def generate_map(w: int, h: int) -> Map:
    if w % 2 == 0:
        w += 1
    if h % 2 == 0:
        h += 1

    maze = [[1 for _ in range(w)] for _ in range(h)]

    def carve(x, y):
        maze[y][x] = 0

        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if 1 <= nx < w - 1 and 1 <= ny < h - 1 and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0
                carve(nx, ny)

    carve(1, 1)

    free_cells = [
        (x, y)
        for y in range(1, h - 1)
        for x in range(1, w - 1)
        if maze[y][x] == 0
    ]

    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        candidates = [(x, 1) for x in range(1, w - 1) if maze[1][x] == 0]
        x, _ = random.choice(candidates)
        maze[0][x] = 0
        exit_pos = (x, 0)

    elif side == "bottom":
        candidates = [(x, h - 2) for x in range(1, w - 1) if maze[h - 2][x] == 0]
        x, _ = random.choice(candidates)
        maze[h - 1][x] = 0
        exit_pos = (x, h - 1)

    elif side == "left":
        candidates = [(1, y) for y in range(1, h - 1) if maze[y][1] == 0]
        _, y = random.choice(candidates)
        maze[y][0] = 0
        exit_pos = (0, y)

    else:
        candidates = [(w - 2, y) for y in range(1, h - 1) if maze[y][w - 2] == 0]
        _, y = random.choice(candidates)
        maze[y][w - 1] = 0
        exit_pos = (w - 1, y)

    px, py = random.choice(free_cells)

    result = Map()
    result.set_player(px, py)
    result.set_exit_pos(*exit_pos)

    for y in range(h):
        for x in range(w):
            if maze[y][x] == 1:
                result.walls.append(Object(x, y))

    return result


class PathfindEngine:
    def __init__(self, executor: Player, map_w: int, map_h: int):
        self.executor = executor
        self.map = generate_map(map_w, map_h)

    def run(self, delay: int = 0.1):
        while self.map.exit_pos.x != self.map.player.x and self.map.exit_pos.y != self.map.player.y:
            self.print_map()
            res = self.executor.think(self.map.player.x, self.map.player.y, self.map.exit_pos.x, self.map.exit_pos.y,
                                self.find_type(self.map.player.x, self.map.player.y + 1),
                                self.find_type(self.map.player.x, self.map.player.y - 1),
                                self.find_type(self.map.player.x + 1, self.map.player.y),
                                self.find_type(self.map.player.x - 1, self.map.player.y)
                                )
            cords = (self.map.player.x, self.map.player.y)
            if res == MoveTo.UP:
                cords = (cords[0], cords[1] + 1)
            elif res == MoveTo.DOWN:
                cords = (cords[0], cords[1] - 1)
            elif res == MoveTo.LEFT:
                cords = (cords[0] - 1, cords[1])
            elif res == MoveTo.RIGHT:
                cords = (cords[0] + 1, cords[1])

            coord_type = self.find_type(cords[0], cords[1])
            print(f"Player position (X, Y): ({self.map.player.x}, {self.map.player.y})")
            print("Moving to (X, Y): ", cords, coord_type)
            if coord_type == CellStatus.WALL:
                raise RuntimeError("Player tried to move into wall!")
            self.map.player.x, self.map.player.y = cords
            print()
            time.sleep(delay)
        print("Player left from maze! Player position was be: ", self.map.player.x, self.map.player.y)

    def find_type(self, x, y) -> CellStatus:
        if self.map.exit_pos.x == x and self.map.exit_pos.y == y:
            return CellStatus.EXIT
        for wall in self.map.walls:
            if wall.x == x and wall.y == y:
                return CellStatus.WALL
        return CellStatus.EMPTY

    def print_map(self):
        map_print = []
        for wall in self.map.walls:
            while len(map_print) < wall.y + 1:
                map_print.append([])
            while len(map_print[wall.y]) < wall.x + 1:
                map_print[wall.y].append([])
            map_print[wall.y][wall.x].append("#")
        map_print[self.map.player.y][self.map.player.x] = "P"
        try:
            map_print[self.map.exit_pos.y][self.map.exit_pos.x] = "█"
        except IndexError:
            self.map = generate_map(len(map_print[0]), len(map_print))
            self.print_map()
            return
        for yy in map_print:
            for xx in yy:
                if len(xx) > 0:
                    print(xx[0], end="")
                else:
                    print(" ", end="")
            print()
