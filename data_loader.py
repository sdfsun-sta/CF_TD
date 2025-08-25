from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Weapon:
    Id: str
    Slot: str
    Type: str
    BaseDamage: float
    HeadshotMult: float
    CritMult: float
    DistanceFalloff: float
    ArmorPen: float
    FireRate: float | None
    Mag: int
    Reload: float
    RefireCD: float | None
    Range: float
    BulletSpeed: float
    AccBase: float
    AccS: float
    AccK: float
    acc_floor: float
    WeakpointRate_Near: float
    WeakpointRate_Mid: float
    WeakpointRate_Far: float
    TurnRate: float
    MultiLock: int
    pierce_cnt: int
    hit_limit: int
    AOERadius: float
    SplashCurveId: str
    Tags: str


def _to_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _to_int(value: str | None) -> int:
    if value is None or value == "":
        return 0
    return int(float(value))


def _validate_weapon(row: dict) -> None:
    fire_rate = _to_float(row.get("FireRate"))
    refire_cd = _to_float(row.get("RefireCD"))
    if (fire_rate is None) == (refire_cd is None):
        raise ValueError(f"Weapon {row.get('Id')} must define exactly one of FireRate or RefireCD")

    armor_pen = float(row.get("ArmorPen", 0))
    if not (0.0 <= armor_pen <= 0.9):
        raise ValueError(f"Weapon {row.get('Id')} ArmorPen {armor_pen} out of range")

    head_mult = float(row.get("HeadshotMult", 0))
    if not (1.5 <= head_mult <= 2.0):
        raise ValueError(f"Weapon {row.get('Id')} HeadshotMult {head_mult} out of range")

    crit_mult = float(row.get("CritMult", 0))
    if not (1.35 <= crit_mult <= 1.5):
        raise ValueError(f"Weapon {row.get('Id')} CritMult {crit_mult} out of range")

    acc_base = float(row.get("AccBase", 0))
    acc_floor = float(row.get("acc_floor", 0))
    if not (0.3 <= acc_floor <= acc_base <= 1.0):
        raise ValueError(
            f"Weapon {row.get('Id')} acc values invalid: acc_base={acc_base}, acc_floor={acc_floor}")

    near = float(row.get("WeakpointRate_Near", 0))
    mid = float(row.get("WeakpointRate_Mid", 0))
    far = float(row.get("WeakpointRate_Far", 0))
    if not (near >= mid >= far):
        raise ValueError(
            f"Weapon {row.get('Id')} weakpoint rates must be monotonic: {near} >= {mid} >= {far}")


def load_weapons(path: Path) -> List[Weapon]:
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        weapons: List[Weapon] = []
        for row in reader:
            _validate_weapon(row)
            weapon = Weapon(
                Id=row["Id"],
                Slot=row["Slot"],
                Type=row["Type"],
                BaseDamage=float(row["BaseDamage"]),
                HeadshotMult=float(row["HeadshotMult"]),
                CritMult=float(row["CritMult"]),
                DistanceFalloff=float(row["DistanceFalloff"]),
                ArmorPen=float(row["ArmorPen"]),
                FireRate=_to_float(row.get("FireRate")),
                Mag=_to_int(row.get("Mag")),
                Reload=float(row.get("Reload", 0)),
                RefireCD=_to_float(row.get("RefireCD")),
                Range=float(row.get("Range", 0)),
                BulletSpeed=float(row.get("BulletSpeed", 0)),
                AccBase=float(row.get("AccBase", 0)),
                AccS=float(row.get("AccS", 0)),
                AccK=float(row.get("AccK", 0)),
                acc_floor=float(row.get("acc_floor", 0)),
                WeakpointRate_Near=float(row.get("WeakpointRate_Near", 0)),
                WeakpointRate_Mid=float(row.get("WeakpointRate_Mid", 0)),
                WeakpointRate_Far=float(row.get("WeakpointRate_Far", 0)),
                TurnRate=float(row.get("TurnRate", 0)),
                MultiLock=_to_int(row.get("MultiLock")),
                pierce_cnt=_to_int(row.get("pierce_cnt")),
                hit_limit=_to_int(row.get("hit_limit")),
                AOERadius=float(row.get("AOERadius", 0)),
                SplashCurveId=row.get("SplashCurveId", ""),
                Tags=row.get("Tags", ""),
            )
            weapons.append(weapon)
    return weapons


# Loaders for other CSVs can be implemented similarly as needed
