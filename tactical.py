"""战术技能模块"""

import csv  # 读取CSV文件
from dataclasses import dataclass  # 数据类装饰器

@dataclass
class Tactical:
    """战术技能数据结构"""
    id: str  # 技能ID
    radius: float  # 作用半径
    delay: float  # 施放延迟
    cooldown: float  # 冷却时间
    energy_cost: float  # 能量消耗
    base_damage: float  # 基础伤害
    special: str  # 特殊规则描述

    @classmethod
    def from_row(cls, row: dict):
        """从CSV行构造战术技能对象"""
        return cls(
            id=row['Id'],  # 技能ID
            radius=float(row['Radius']),  # 作用半径
            delay=float(row['Delay']),  # 施放延迟
            cooldown=float(row['Cooldown']),  # 冷却时间
            energy_cost=float(row['EnergyCost']),  # 能量消耗
            base_damage=float(row['BaseDamage']),  # 基础伤害
            special=row['SpecialRules'],  # 特殊规则
        )

def load_tacticals(path: str) -> dict[str, Tactical]:
    """加载战术技能配置表"""
    with open(path, newline='') as f:  # 打开文件
        reader = csv.DictReader(f)  # CSV读取器
        return {row['Id']: Tactical.from_row(row) for row in reader}  # 构造字典返回
