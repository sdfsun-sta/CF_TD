import csv
from dataclasses import dataclass

@dataclass
class Enemy:
    id: str
    hp: float
    armor_dr: float
    speed: float
    leak_damage: float
    pos: float = 30.0  # starting distance

    def update(self, dt: float):
        self.pos -= self.speed * dt

    def apply_damage(self, dmg: float, armor_pen: float):
        effective = dmg * armor_pen * (1 - self.armor_dr)
        self.hp -= effective
        return effective

    @property
    def alive(self) -> bool:
        return self.hp > 0

    @property
    def leaked(self) -> bool:
        return self.pos <= 0 and self.alive

    @classmethod
    def from_row(cls, row: dict):
        return cls(
            id=row['Id'],
            hp=float(row['HP']),
            armor_dr=float(row['ArmorDR']),
            speed=float(row['Speed']),
            leak_damage=float(row['LeakDamage']),
        )


def load_enemies(path: str) -> dict[str, Enemy]:
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        return {row['Id']: Enemy.from_row(row) for row in reader}
