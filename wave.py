import csv
from dataclasses import dataclass
from collections import deque

@dataclass
class SpawnEvent:
    time: float
    enemy_id: str

@dataclass
class WaveRecipe:
    wave: int
    duration: float
    spawn_events: deque[SpawnEvent]

    @classmethod
    def from_row(cls, row: dict):
        events = deque()
        spawn_str = row['SpawnList']
        t = 0.0
        for part in spawn_str.split('|'):
            name,count = part.split('*')
            for _ in range(int(count)):
                events.append(SpawnEvent(time=t, enemy_id=name))
                t += 1.0
        return cls(
            wave=int(row['Wave']),
            duration=float(row['Duration']),
            spawn_events=events,
        )


def load_waves(path: str) -> dict[int, WaveRecipe]:
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        return {int(row['Wave']): WaveRecipe.from_row(row) for row in reader}
