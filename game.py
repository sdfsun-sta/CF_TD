from dataclasses import dataclass
from weapon import Weapon
from enemy import Enemy


@dataclass
class Game:
    """Simple game loop that processes weapon fire against an enemy."""

    weapon: Weapon
    enemy: Enemy

    def loop(self):
        """Simulate a single bullet fired from the weapon at the enemy.

        The method uses the weapon's :meth:`hit` to determine if the bullet
        lands and whether it strikes a weakpoint. Damage is calculated per
        bullet and armour is taken into account. The enemy's remaining HP is
        returned for external feedback (e.g., to show "hit" or "headshot" messages).

        Returns
        -------
        dict
            A dictionary containing the results of the shot with the keys:
            ``hit`` (bool), ``weakpoint`` (bool), ``damage`` (float) and
            ``enemy_hp`` (float).
        """
        hit, weakpoint = self.weapon.hit()
        if not hit:
            remaining = self.enemy.apply_damage(0)
            return {"hit": False, "weakpoint": False, "damage": 0.0, "enemy_hp": remaining}

        damage = self.weapon.damage()
        if weakpoint:
            damage *= self.weapon.weakpoint_multiplier()

        damage = max(damage - getattr(self.enemy, "armor", 0), 0)
        remaining = self.enemy.apply_damage(damage)

        return {"hit": True, "weakpoint": weakpoint, "damage": damage, "enemy_hp": remaining}
