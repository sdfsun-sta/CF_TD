import csv
from dataclasses import dataclass

@dataclass
class Weapon:
    id: str
    base_damage: float
    headshot_mult: float
    falloff: float
    armor_pen: float
    fire_rate: float | None
    refire_cd: float | None
    range: float
    bullet_speed: float
    acc_base: float
    acc_s: float
    acc_k: float
    acc_floor: float
    weak_near: float
    weak_mid: float
    weak_far: float

    def accuracy(self, distance: float) -> float:
        if distance <= self.acc_s:
            acc = self.acc_base
        else:
            acc = self.acc_base - self.acc_k * (distance - self.acc_s)
        return max(self.acc_floor, acc)

    def weakpoint_rate(self, distance: float) -> float:
        if distance <= 6:
            return self.weak_near
        if distance <= 12:
            return self.weak_mid
        return self.weak_far

    def damage_at(self, distance: float, weakpoint: bool) -> float:
        dmg = max(0.0, self.base_damage - distance * self.falloff)
        if weakpoint:
            dmg *= self.headshot_mult
        return dmg

    @classmethod
    def from_row(cls, row: dict):
        return cls(
            id=row['Id'],
            base_damage=float(row['BaseDamage']),
            headshot_mult=float(row['HeadshotMult']),
            falloff=float(row['DistanceFalloff']),
            armor_pen=float(row['ArmorPen']),
            fire_rate=float(row['FireRate']) if row['FireRate'] else None,
            refire_cd=float(row['RefireCD']) if row['RefireCD'] else None,
            range=float(row['Range']),
            bullet_speed=float(row['BulletSpeed']),
            acc_base=float(row['AccBase']),
            acc_s=float(row['AccS']),
            acc_k=float(row['AccK']),
            acc_floor=float(row['acc_floor']),
            weak_near=float(row['WeakpointRate_Near']),
            weak_mid=float(row['WeakpointRate_Mid']),
            weak_far=float(row['WeakpointRate_Far']),
        )


def load_weapons(path: str) -> dict[str, Weapon]:
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        return {row['Id']: Weapon.from_row(row) for row in reader}
