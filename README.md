# pathfind_engine_task
## Install
```commandline
pip install git+https://github.com/RoboStartCoder/pathfind_engine_task.git
```

## Example
```python
from pathfind_engine.PathfindEngine import PathfindEngine
from pathfind_engine.api.Executor import Player

MAP_W, MAP_H = 16, 8

class Executor(Player):
    def __init__(self):
        self.visited = set()

    def think(self, x, y, exit_x, exit_y, up, down, right, left):
        return None


if __name__ == '__main__':
    eng = PathfindEngine(Executor(), MAP_W, MAP_H)
    eng.run()
```