from weapon import load_weapons
from enemy import load_enemies, Enemy
from wave import load_waves

DT = 0.1

class Game:
    def __init__(self):
        self.weapons = load_weapons('data/Weapon.csv')
        self.enemies_def = load_enemies('data/Enemy.csv')
        self.waves = load_waves('data/WaveRecipe.csv')
        self.wall_hp = 100
        self.coins = 0

    def spawn_enemy(self, enemy_id: str) -> Enemy:
        base = self.enemies_def[enemy_id]
        return Enemy(id=base.id, hp=base.hp, armor_dr=base.armor_dr, speed=base.speed, leak_damage=base.leak_damage)

    def run_wave(self, wave_id: int):
        recipe = self.waves[wave_id]
        weapon = self.weapons['AR']
        enemies: list[Enemy] = []
        time = 0.0
        fire_cd = 0.0
        events = recipe.spawn_events.copy()
        while time < recipe.duration or enemies:
            # spawn
            while events and events[0].time <= time:
                ev = events.popleft()
                enemies.append(self.spawn_enemy(ev.enemy_id))
            # update enemies
            for e in list(enemies):
                e.update(DT)
                if e.leaked:
                    self.wall_hp -= e.leak_damage
                    enemies.remove(e)
                elif not e.alive:
                    self.coins += 1
                    enemies.remove(e)
            if self.wall_hp <= 0:
                print('Wall destroyed')
                return
            # fire weapon
            if fire_cd <= 0 and enemies:
                target = min(enemies, key=lambda e: e.pos)
                dist = target.pos
                acc = weapon.accuracy(dist)
                weak_rate = weapon.weakpoint_rate(dist)
                dmg_weak = weapon.damage_at(dist, True)
                dmg_body = weapon.damage_at(dist, False)
                expected = acc * (weak_rate * dmg_weak + (1 - weak_rate) * dmg_body)
                dealt = target.apply_damage(expected, weapon.armor_pen)
                fire_cd = 1.0 / weapon.fire_rate if weapon.fire_rate else weapon.refire_cd
            else:
                fire_cd -= DT
            time += DT
        print(f"Wave {wave_id} complete. Wall HP={self.wall_hp}, coins={self.coins}")


def main():
    g = Game()
    g.run_wave(1)

if __name__ == '__main__':
    main()
