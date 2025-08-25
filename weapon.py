import random

class Weapon:
    """Represents a weapon that fires individual bullets.

    Parameters
    ----------
    damage: float
        Base damage dealt by each bullet.
    accuracy: float
        Probability in the range [0, 1] that a bullet hits the target.
    weakpoint_rate: float
        Probability in the range [0, 1] that a hit bullet strikes a weakpoint.
    weakpoint_multiplier: float, optional
        Damage multiplier applied when a weakpoint is hit. Defaults to 2.
    """

    def __init__(self, damage, accuracy, weakpoint_rate, weakpoint_multiplier=2.0):
        self._damage = damage
        self._accuracy = accuracy
        self._weakpoint_rate = weakpoint_rate
        self._weakpoint_multiplier = weakpoint_multiplier

    def damage(self):
        """Return base damage of a bullet."""
        return self._damage

    def accuracy(self):
        """Return the accuracy of the weapon."""
        return self._accuracy

    def weakpoint_rate(self):
        """Return probability of hitting a weakpoint on hit."""
        return self._weakpoint_rate

    def weakpoint_multiplier(self):
        """Return damage multiplier applied on weakpoint hit."""
        return self._weakpoint_multiplier

    def hit(self):
        """Determine whether a bullet hits and if it strikes a weakpoint.

        Returns
        -------
        tuple(bool, bool)
            A tuple ``(hit, weakpoint)`` where ``hit`` indicates whether the
            bullet hit the target and ``weakpoint`` indicates whether the hit
            was on a weakpoint. ``weakpoint`` is ``False`` when ``hit`` is
            ``False``.
        """
        is_hit = random.random() <= self.accuracy()
        is_weakpoint = False
        if is_hit:
            is_weakpoint = random.random() <= self.weakpoint_rate()
        return is_hit, is_weakpoint
