import os
from pathlib import Path
import unittest

from game import Game, Enemy


class TestTacticals(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        path = Path(__file__).resolve().parent.parent / "skills.json"
        self.game.load_tacticals(path)

    def test_cast_damage_and_cooldown(self):
        enemies = [Enemy()]
        self.game.energy = 50
        result = self.game.cast_tactical("fireball", enemies)
        self.assertTrue(result)
        self.assertEqual(enemies[0].hp, 50)
        self.assertGreater(self.game.cooldowns["fireball"], 0)
        self.assertEqual(self.game.energy, 30)

    def test_cast_stun_and_slow(self):
        enemy = Enemy()
        self.game.energy = 100
        self.assertTrue(self.game.cast_tactical("stun", [enemy]))
        self.assertTrue(enemy.stunned)
        self.assertIn("slow", enemy.statuses)

    def test_update_energy_and_cooldown(self):
        self.game.energy = 0
        self.game.update(1.0)
        self.assertEqual(self.game.energy, min(self.game.energy_max, 10))
        self.game.cooldowns["fireball"] = 1.0
        self.game.update(0.5)
        self.assertAlmostEqual(self.game.cooldowns["fireball"], 0.5)

    def test_enemy_status_decay(self):
        enemy = Enemy()
        enemy.apply_status("slow", 1.0, multiplier=0.5)
        enemy.apply_status("stun", 0.5)
        enemy.update(0.5)
        self.assertNotIn("stun", enemy.statuses)
        enemy.update(0.5)
        self.assertNotIn("slow", enemy.statuses)


if __name__ == "__main__":
    unittest.main()
