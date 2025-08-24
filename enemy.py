"""敌人模块"""

import csv  # 读取CSV文件
from dataclasses import dataclass  # 数据类装饰器

@dataclass
class Enemy:
    """敌人数据结构"""
    id: str  # 敌人ID
    hp: float  # 生命值
    armor_dr: float  # 护甲减伤比例
    speed: float  # 移动速度
    leak_damage: float  # 泄露时对城墙造成的伤害
    pos: float = 30.0  # 起始距离

    def update(self, dt: float):
        """根据时间步长更新位置"""
        self.pos -= self.speed * dt  # 向城墙移动

    def apply_damage(self, dmg: float, armor_pen: float):
        """结算伤害并返回实际造成的伤害"""
        effective = dmg * armor_pen * (1 - self.armor_dr)  # 实际伤害
        self.hp -= effective  # 扣除生命值
        return effective  # 返回实际伤害

    @property
    def alive(self) -> bool:
        """是否存活"""
        return self.hp > 0

    @property
    def leaked(self) -> bool:
        """是否已经到达城墙"""
        return self.pos <= 0 and self.alive

    @classmethod
    def from_row(cls, row: dict):
        """从CSV行构造敌人对象"""
        return cls(
            id=row['Id'],  # 敌人ID
            hp=float(row['HP']),  # 生命值
            armor_dr=float(row['ArmorDR']),  # 护甲减伤
            speed=float(row['Speed']),  # 移动速度
            leak_damage=float(row['LeakDamage']),  # 泄露伤害
        )

def load_enemies(path: str) -> dict[str, Enemy]:
    """加载敌人配置表"""
    with open(path, newline='') as f:  # 打开文件
        reader = csv.DictReader(f)  # CSV读取器
        return {row['Id']: Enemy.from_row(row) for row in reader}  # 构造字典返回
