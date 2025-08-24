import csv
from dataclasses import dataclass

@dataclass
class Tactical:
    id: str
    radius: float
    delay: float
    cooldown: float
    energy_cost: float
    base_damage: float
    special: str

    @classmethod
    def from_row(cls, row: dict):
        return cls(
            id=row['Id'],
            radius=float(row['Radius']),
            delay=float(row['Delay']),
            cooldown=float(row['Cooldown']),
            energy_cost=float(row['EnergyCost']),
            base_damage=float(row['BaseDamage']),
            special=row['SpecialRules'],
        )


def load_tacticals(path: str) -> dict[str, Tactical]:
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        return {row['Id']: Tactical.from_row(row) for row in reader}
