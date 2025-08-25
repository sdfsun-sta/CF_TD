import random
import unittest

from battle import Gun, Monster, fire


class BattleTest(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(0)

    def test_hit_and_damage(self):
        gun = Gun(
            name="pistol",
            accuracy=1.0,
            fire_rate=1.0,
            bullet_damage=10.0,
            bullet_speed=10.0,
            headshot_chance=0.0,
            damage_decay_per_meter=0.0,
            accuracy_decay_per_meter=0.0,
        )
        monster = Monster(health=20.0, speed=0.0, distance=10.0)
        bullet = fire(gun, monster, monster.distance, self.rng)
        self.assertTrue(bullet.hit)
        self.assertAlmostEqual(bullet.time_to_hit, 1.0)
        monster.health -= bullet.damage
        self.assertEqual(monster.health, 10.0)

    def test_miss_due_to_accuracy(self):
        gun = Gun(
            name="pistol",
            accuracy=0.0,
            fire_rate=1.0,
            bullet_damage=10.0,
            bullet_speed=10.0,
            headshot_chance=0.0,
            damage_decay_per_meter=0.0,
            accuracy_decay_per_meter=0.0,
        )
        monster = Monster(health=20.0, speed=0.0, distance=5.0)
        bullet = fire(gun, monster, monster.distance, self.rng)
        self.assertFalse(bullet.hit)
        self.assertEqual(bullet.damage, 0.0)

    def test_headshot_damage(self):
        gun = Gun(
            name="sniper",
            accuracy=1.0,
            fire_rate=1.0,
            bullet_damage=10.0,
            bullet_speed=10.0,
            headshot_chance=1.0,
            damage_decay_per_meter=0.0,
            accuracy_decay_per_meter=0.0,
        )
        monster = Monster(health=30.0, speed=0.0, distance=5.0, headshot_multiplier=2.5)
        bullet = fire(gun, monster, monster.distance, self.rng)
        self.assertTrue(bullet.hit)
        self.assertEqual(bullet.damage, 25.0)

    def test_damage_decay(self):
        gun = Gun(
            name="rifle",
            accuracy=1.0,
            fire_rate=1.0,
            bullet_damage=20.0,
            bullet_speed=10.0,
            headshot_chance=0.0,
            damage_decay_per_meter=1.0,
            accuracy_decay_per_meter=0.0,
        )
        monster = Monster(health=50.0, speed=0.0, distance=3.0)
        bullet = fire(gun, monster, monster.distance, self.rng)
        self.assertTrue(bullet.hit)
        self.assertEqual(bullet.damage, 17.0)


if __name__ == "__main__":
    unittest.main()
