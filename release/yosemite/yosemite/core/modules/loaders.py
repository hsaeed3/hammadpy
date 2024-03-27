from yosemite.core.modules.text import Text
import threading
import time
import sys

class Status:
    """Displays a simple animated loading placeholder."""

    def __init__(self, message: str = "Loading...", color: str = "white", animation: str = "|/-\\", styles: str = None):
        self.say = Text()
        self.timer = Timer()
        self.message = message
        self.color = color
        self.animation = animation
        self.is_running = False
        self.index = 0

        animations = {
            "blocks": "█▉▊▋▌▍▎▏ ",
            "emoji": "🌑🌒🌓🌔🌕🌖🌗🌘",
            "hourglass": "⏳⌛",
            "dots": "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
            "arrows": "←↖↑↗→↘↓↙",
            "lines": "┤┘┴└├┌┬┐",
            "pipes": "┃┃┃┃┃┃┃┃┃",
            "dots2": "⣾⣽⣻⢿⡿⣟⣯⣷",
            "dots3": "⢄⢂⢁⡁⡈⡐⡠",
            "stars": "✶✸✹✺✹✷",
            "ping": "⚫⚪",
            "hearts": "💗💓💕💖💞💘💝💟",
            "weather": "🌤️🌥️🌦️🌧️⛈️🌩️🌨️☃️",
            "moons": "🌑🌒🌓🌔🌕🌖🌗🌘🌑"
        }

        if styles in animations:
            self.animation = animations[styles]

    def __enter__(self):
        self.timer.enter()
        self.is_running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()
        return self

    def _animate(self):
        while self.is_running:
            sys.stdout.write(f"\r{self.message} {self.animation[self.index]}")
            sys.stdout.flush()
            time.sleep(0.1)
            self.index = (self.index + 1) % len(self.animation)

    def __exit__(self, exc_type, exc_value, traceback):
        self.is_running = False
        self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\n")
        self.timer.exit()

    def checkpoint(self, message: str):
        """Displays a checkpoint message while the status is running."""
        self.is_running = False
        self.thread.join()
        checkpoint_message = f"\r{self.message} {message}\n"
        sys.stdout.write(checkpoint_message)
        sys.stdout.flush()
        time.sleep(1)
        self.is_running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

class Timer:
    """Measures and prints the execution time of a task."""

    def __init__(self, message: str = "Task"):
        self.say = Text()
        self.message = message

    def enter(self):
        self.start_time = time.time()
        return self

    def exit(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        message = f"{self.message} completed in {elapsed_time:.2f} seconds."
        self.say.say(message, color="green", bold=True)

if __name__ == "__main__":
    status = Status(styles="blocks")
    timer = Timer()

    with status:
        time.sleep(2)
        status.checkpoint("Checkpoint 1")
        time.sleep(2)