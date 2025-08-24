from dataclasses import dataclass
import random
from typing import List, Optional


@dataclass
class Gun:
    """Representation of a firearm used by the player."""
    name: str
    accuracy: float  # Base chance to hit at zero distance (0-1)
    fire_rate: float  # Rounds per second
    bullet_damage: float  # Damage per bullet before modifiers
    bullet_speed: float  # Units per second
    headshot_chance: float  # Chance for headshot (0-1)
    damage_decay_per_meter: float  # Damage lost per meter of distance
    accuracy_decay_per_meter: float  # Accuracy lost per meter of distance

    def time_between_shots(self) -> float:
        """Time delay between two shots."""
        return 1.0 / self.fire_rate


@dataclass
class Monster:
    """A monster advancing towards the player."""
    health: float
    speed: float  # Units per second towards the player
    distance: float  # Current distance from the player
    headshot_multiplier: float = 2.0

    def is_alive(self) -> bool:
        return self.health > 0


@dataclass
class Bullet:
    """Bullet travelling towards a monster."""
    target: Monster
    time_to_hit: float  # Seconds until bullet reaches target
    damage: float
    hit: bool


def fire(gun: Gun, target: Monster, distance: float, rng: random.Random) -> Bullet:
    """Fire a single bullet towards the target at the given distance."""
    hit_probability = max(0.0, gun.accuracy - gun.accuracy_decay_per_meter * distance)
    hit = rng.random() <= hit_probability
    damage = 0.0
    if hit:
        damage = max(0.0, gun.bullet_damage - gun.damage_decay_per_meter * distance)
        if rng.random() <= gun.headshot_chance:
            damage *= target.headshot_multiplier
    time_to_hit = distance / gun.bullet_speed
    return Bullet(target=target, time_to_hit=time_to_hit, damage=damage, hit=hit)


def simulate_battle(gun: Gun, monsters: List[Monster], rng: Optional[random.Random] = None) -> tuple[bool, float]:
    """Simulate a battle against a list of monsters.

    Returns a tuple (player_survived, time_elapsed).
    """
    if rng is None:
        rng = random.Random()

    time_elapsed = 0.0
    bullets: List[Bullet] = []
    dt = gun.time_between_shots()

    while any(m.is_alive() and m.distance > 0 for m in monsters):
        # Resolve bullets in flight
        for b in list(bullets):
            b.time_to_hit -= dt
            if b.time_to_hit <= 0:
                if b.hit and b.target.is_alive():
                    b.target.health -= b.damage
                bullets.remove(b)

        # Advance monsters
        for m in monsters:
            if m.is_alive():
                m.distance -= m.speed * dt
                if m.distance <= 0:
                    return False, time_elapsed

        # Choose the closest living target
        living = [m for m in monsters if m.is_alive()]
        if not living:
            break
        target = min(living, key=lambda m: m.distance)

        # Fire a new bullet
        bullets.append(fire(gun, target, target.distance, rng))
        time_elapsed += dt

    # Resolve any bullets still in the air after the last shot
    for b in bullets:
        time_elapsed += b.time_to_hit
        if b.hit and b.target.is_alive():
            b.target.health -= b.damage
        # Check if any monster reaches the player during remaining bullet flight
        for m in monsters:
            if m.is_alive():
                m.distance -= m.speed * b.time_to_hit
                if m.distance <= 0:
                    return False, time_elapsed

    return True, time_elapsed
