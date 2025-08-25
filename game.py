import json
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class Skill:
    """Data for a tactical skill."""
    id: str
    energy_cost: float
    cooldown: float
    damage: float = 0
    stun_duration: float = 0
    slow_duration: float = 0
    slow_multiplier: float = 1.0


class Enemy:
    """Basic enemy supporting status effects."""

    def __init__(self, hp: float = 100, speed: float = 1.0) -> None:
        self.hp = hp
        self.base_speed = speed
        # status name -> data dict with remaining duration and params
        self.statuses: Dict[str, Dict[str, Any]] = {}

    def take_damage(self, amount: float) -> None:
        self.hp = max(0, self.hp - amount)

    def apply_status(self, name: str, duration: float, **params: Any) -> None:
        """Apply a named status effect with given duration and optional params."""
        self.statuses[name] = {"duration": duration, **params}

    def update(self, dt: float) -> None:
        """Update all active status effects, reducing remaining durations."""
        expired = []
        for name, data in self.statuses.items():
            data["duration"] -= dt
            if data["duration"] <= 0:
                expired.append(name)
        for name in expired:
            del self.statuses[name]

    @property
    def stunned(self) -> bool:
        return "stun" in self.statuses

    @property
    def speed(self) -> float:
        if self.stunned:
            return 0.0
        multiplier = 1.0
        slow = self.statuses.get("slow")
        if slow:
            multiplier *= slow.get("multiplier", 1.0)
        return self.base_speed * multiplier


class Game:
    """Game container tracking energy and skill cooldowns."""

    def __init__(self, energy_max: float = 100, energy_recovery: float = 10.0) -> None:
        self.energy_max = energy_max
        self.energy_recovery = energy_recovery
        self.energy = energy_max
        self.tacticals: Dict[str, Skill] = {}
        self.cooldowns: Dict[str, float] = {}

    def load_tacticals(self, path: str) -> None:
        """Load tactical skill definitions from a JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for entry in data:
            skill = Skill(**entry)
            self.tacticals[skill.id] = skill
            self.cooldowns.setdefault(skill.id, 0)

    def cast_tactical(self, skill_id: str, enemies: List[Enemy]) -> bool:
        """Attempt to cast a tactical skill on the provided enemies.

        Returns True if the skill was cast successfully, otherwise False.
        """
        skill = self.tacticals.get(skill_id)
        if not skill:
            return False
        # Check energy and cooldown
        if self.energy < skill.energy_cost or self.cooldowns.get(skill_id, 0) > 0:
            return False
        # Spend energy and set cooldown
        self.energy -= skill.energy_cost
        self.cooldowns[skill_id] = skill.cooldown

        # Apply effects to enemies
        for enemy in enemies:
            if skill.damage:
                enemy.take_damage(skill.damage)
            if skill.stun_duration:
                enemy.apply_status("stun", skill.stun_duration)
            if skill.slow_duration and skill.slow_multiplier < 1:
                enemy.apply_status("slow", skill.slow_duration, multiplier=skill.slow_multiplier)
        return True

    def update(self, dt: float) -> None:
        """Recover energy and decrement skill cooldowns."""
        self.energy = min(self.energy_max, self.energy + self.energy_recovery * dt)
        for skill_id, cd in list(self.cooldowns.items()):
            if cd > 0:
                self.cooldowns[skill_id] = max(0, cd - dt)
