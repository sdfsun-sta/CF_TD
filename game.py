import sys
import time
import select
import termios
import tty


class Game:
    def __init__(self):
        self.waves = [5, 7, 6]
        self.current_wave = 0
        self.wall_hp = 20
        self.attack_priorities = ["closest", "strongest"]
        self.priority_index = 0
        self.enemy_count = self.waves[self.current_wave]
        self.paused = False

    def toggle_priority(self):
        self.priority_index = (self.priority_index + 1) % len(self.attack_priorities)

    def use_skill(self, index: int):
        print(f"Used skill {index}")

    def update(self, dt: float):
        if self.enemy_count > 0:
            self.enemy_count -= 1
            self.wall_hp -= 1
        else:
            self.current_wave += 1
            if self.current_wave < len(self.waves):
                self.enemy_count = self.waves[self.current_wave]

    def render(self):
        print(
            f"Wave {self.current_wave + 1}/{len(self.waves)} | "
            f"Wall HP: {self.wall_hp} | "
            f"Enemies: {self.enemy_count} | "
            f"Priority: {self.attack_priorities[self.priority_index]}"
        )

    def is_over(self) -> bool:
        return self.wall_hp <= 0 or self.current_wave >= len(self.waves)


def get_key():
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    if dr:
        return sys.stdin.read(1)
    return None


def main():
    game = Game()
    dt = 0.5
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    try:
        while not game.is_over():
            start = time.time()
            key = get_key()
            if key:
                key = key.upper()
                if key == "Q":
                    game.toggle_priority()
                elif key in {"1", "2", "3", "4"}:
                    game.use_skill(int(key))
                elif key == " ":
                    game.paused = not game.paused
            if not game.paused:
                game.update(dt)
            game.render()
            elapsed = time.time() - start
            if elapsed < dt:
                time.sleep(dt - elapsed)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


if __name__ == "__main__":
    main()
