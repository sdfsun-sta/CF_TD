"""武器系统模块"""

import csv  # 读取CSV数据
from dataclasses import dataclass  # 使用数据类保存武器信息

@dataclass
class Weapon:
    """武器数据结构，存储所有武器参数"""
    id: str  # 武器ID
    base_damage: float  # 基础伤害
    headshot_mult: float  # 爆头倍率
    falloff: float  # 距离衰减系数
    armor_pen: float  # 护甲穿透率
    fire_rate: float | None  # 射速，和refire_cd互斥
    refire_cd: float | None  # 射击间隔，fire_rate为空时使用
    range: float  # 射程
    bullet_speed: float  # 子弹速度
    acc_base: float  # 基础命中率
    acc_s: float  # 命中率拐点距离
    acc_k: float  # 命中率衰减斜率
    acc_floor: float  # 命中率下限
    weak_near: float  # 近距离弱点率
    weak_mid: float  # 中距离弱点率
    weak_far: float  # 远距离弱点率

    def accuracy(self, distance: float) -> float:
        """根据距离计算命中率"""
        if distance <= self.acc_s:
            acc = self.acc_base  # 使用基础命中率
        else:
            acc = self.acc_base - self.acc_k * (distance - self.acc_s)  # 计算衰减后的命中率
        return max(self.acc_floor, acc)  # 不低于命中下限

    def weakpoint_rate(self, distance: float) -> float:
        """根据距离返回弱点触发率"""
        if distance <= 6:
            return self.weak_near  # 近距离
        if distance <= 12:
            return self.weak_mid  # 中距离
        return self.weak_far  # 远距离

    def damage_at(self, distance: float, weakpoint: bool) -> float:
        """计算指定距离的伤害，weakpoint 表示是否命中弱点"""
        dmg = max(0.0, self.base_damage - distance * self.falloff)  # 距离衰减后的伤害
        if weakpoint:
            dmg *= self.headshot_mult  # 弱点倍率
        return dmg

    @classmethod
    def from_row(cls, row: dict):
        """从CSV行构造武器对象"""
        return cls(
            id=row['Id'],  # 武器ID
            base_damage=float(row['BaseDamage']),  # 基础伤害
            headshot_mult=float(row['HeadshotMult']),  # 爆头倍率
            falloff=float(row['DistanceFalloff']),  # 距离衰减
            armor_pen=float(row['ArmorPen']),  # 护甲穿透率
            fire_rate=float(row['FireRate']) if row['FireRate'] else None,  # 射速
            refire_cd=float(row['RefireCD']) if row['RefireCD'] else None,  # 射击间隔
            range=float(row['Range']),  # 射程
            bullet_speed=float(row['BulletSpeed']),  # 子弹速度
            acc_base=float(row['AccBase']),  # 基础命中率
            acc_s=float(row['AccS']),  # 命中率拐点距离
            acc_k=float(row['AccK']),  # 命中率衰减斜率
            acc_floor=float(row['acc_floor']),  # 命中率下限
            weak_near=float(row['WeakpointRate_Near']),  # 近距弱点率
            weak_mid=float(row['WeakpointRate_Mid']),  # 中距弱点率
            weak_far=float(row['WeakpointRate_Far']),  # 远距弱点率
        )

def load_weapons(path: str) -> dict[str, Weapon]:
    """加载武器配置表"""
    with open(path, newline='') as f:  # 打开文件
        reader = csv.DictReader(f)  # CSV读取器
        return {row['Id']: Weapon.from_row(row) for row in reader}  # 构造武器字典
