"""波次配置模块"""

import csv  # 读取CSV文件
from dataclasses import dataclass  # 数据类装饰器
from collections import deque  # 双端队列

@dataclass
class SpawnEvent:
    """单次刷怪事件"""
    time: float  # 触发时间
    enemy_id: str  # 敌人ID

@dataclass
class WaveRecipe:
    """波次配置数据"""
    wave: int  # 波次编号
    duration: float  # 波次持续时间
    spawn_events: deque[SpawnEvent]  # 刷怪事件队列

    @classmethod
    def from_row(cls, row: dict):
        """从CSV行构造波次配置"""
        events = deque()  # 刷怪事件队列
        spawn_str = row['SpawnList']  # 刷怪描述字符串
        t = 0.0  # 当前时间
        for part in spawn_str.split('|'):
            name, count = part.split('*')  # 敌人ID与数量
            for _ in range(int(count)):
                events.append(SpawnEvent(time=t, enemy_id=name))  # 添加事件
                t += 1.0  # 下一次刷怪时间
        return cls(
            wave=int(row['Wave']),  # 波次编号
            duration=float(row['Duration']),  # 持续时间
            spawn_events=events,  # 事件队列
        )

def load_waves(path: str) -> dict[int, WaveRecipe]:
    """加载波次配置表"""
    with open(path, newline='') as f:  # 打开文件
        reader = csv.DictReader(f)  # CSV读取器
        return {int(row['Wave']): WaveRecipe.from_row(row) for row in reader}  # 构造字典
