"""简易塔防游戏主循环"""

from weapon import load_weapons  # 读取武器配置
from enemy import load_enemies, Enemy  # 读取敌人配置及敌人类
from wave import load_waves  # 读取波次配置

DT = 0.1  # 每帧时间步长

class Game:
    """游戏主类"""
    def __init__(self):
        """初始化游戏数据"""
        self.weapons = load_weapons('data/Weapon.csv')  # 武器字典
        self.enemies_def = load_enemies('data/Enemy.csv')  # 敌人模板字典
        self.waves = load_waves('data/WaveRecipe.csv')  # 波次配置字典
        self.wall_hp = 100  # 城墙生命值
        self.coins = 0  # 金币数量

    def spawn_enemy(self, enemy_id: str) -> Enemy:
        """根据ID生成敌人实例"""
        base = self.enemies_def[enemy_id]  # 获取模板
        return Enemy(id=base.id, hp=base.hp, armor_dr=base.armor_dr,
                     speed=base.speed, leak_damage=base.leak_damage)  # 返回复制体

    def run_wave(self, wave_id: int):
        """运行指定波次"""
        recipe = self.waves[wave_id]  # 当前波次配置
        weapon = self.weapons['AR']  # 使用的武器
        enemies: list[Enemy] = []  # 场上敌人列表
        time = 0.0  # 当前时间
        fire_cd = 0.0  # 射击冷却计时
        events = recipe.spawn_events.copy()  # 剩余刷怪事件
        while time < recipe.duration or enemies:  # 波次循环
            # spawn
            while events and events[0].time <= time:
                ev = events.popleft()  # 获取事件
                enemies.append(self.spawn_enemy(ev.enemy_id))  # 生成敌人
            # update enemies
            for e in list(enemies):
                e.update(DT)  # 更新位置
                if e.leaked:
                    self.wall_hp -= e.leak_damage  # 城墙受损
                    enemies.remove(e)  # 移除敌人
                elif not e.alive:
                    self.coins += 1  # 击杀奖励
                    enemies.remove(e)
            if self.wall_hp <= 0:
                print('Wall destroyed')  # 城墙被摧毁
                return
            # fire weapon
            if fire_cd <= 0 and enemies:
                target = min(enemies, key=lambda e: e.pos)  # 选择最近敌人
                dist = target.pos  # 目标距离
                acc = weapon.accuracy(dist)  # 命中率
                weak_rate = weapon.weakpoint_rate(dist)  # 弱点触发率
                dmg_weak = weapon.damage_at(dist, True)  # 弱点伤害
                dmg_body = weapon.damage_at(dist, False)  # 身体伤害
                expected = acc * (weak_rate * dmg_weak + (1 - weak_rate) * dmg_body)  # 期望伤害
                dealt = target.apply_damage(expected, weapon.armor_pen)  # 实际伤害
                fire_cd = 1.0 / weapon.fire_rate if weapon.fire_rate else weapon.refire_cd  # 重置冷却
            else:
                fire_cd -= DT  # 冷却递减
            time += DT  # 时间推进
        print(f"Wave {wave_id} complete. Wall HP={self.wall_hp}, coins={self.coins}")  # 波次结束

def main():
    """程序入口"""
    g = Game()  # 创建游戏对象
    g.run_wave(1)  # 运行第一波

if __name__ == '__main__':
    main()  # 启动游戏
