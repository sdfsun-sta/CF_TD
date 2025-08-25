class Enemy:
    """Represents an enemy target with health and optional armor."""

    def __init__(self, hp, armor=0.0):
        self.hp = hp
        self.armor = armor

    def apply_damage(self, damage):
        """Apply damage to the enemy and return remaining HP.

        Parameters
        ----------
        damage: float
            The amount of damage to subtract from the enemy's HP.

        Returns
        -------
        float
            The remaining HP after damage is applied. HP will not drop below
            zero.
        """
        self.hp = max(self.hp - damage, 0)
        return self.hp
