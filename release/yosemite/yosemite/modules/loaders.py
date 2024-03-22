from yosemite.modules.text import Text
import threading
import time

"""
hammadcore.modules.loaders

This module contains classes for displaying loading animations and timers in the CLI.

Example:
    # Status
    with Status(message="Loading...") as status:
        # Perform some operation
        pass

    # Timer
    with Timer(message="Task") as timer:
        # Perform some operation
        pass
        
Attributes:
    Status: A class for displaying a simple animated loading placeholder.
    Timer: A class for measuring and printing the execution time of a task.
"""

class Status:
    """Displays a simple animated loading placeholder."""

    def __init__(self, message: str = "Loading...", color: str = "white", animation: str = "|/-\\", styles: str = None):
        """
        Initializes the loading placeholder.

        Args:
            message (str, optional): The message to display alongside the animation.
            animation (str, optional):  A sequence of characters for the animation.
            styles (str, optional): The style of the loading animation.
        """
        self.say = Text()
        self.timer = Timer()
        self.message = message
        self.color = color
        self.animation = animation
        self.is_running = False  
        self.index = 0  

        if styles == "blocks":
            self.animation = "█▉▊▋▌▍▎▏ "
        elif styles == "emoji":
            self.animation = "🌑🌒🌓🌔🌕🌖🌗🌘"
        elif styles == "hourglass":
            self.animation = "⏳⌛"
        elif styles == "dots":
            self.animation = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        elif styles == "arrows":
            self.animation = "←↖↑↗→↘↓↙"
        elif styles == "lines":
            self.animation = "┤┘┴└├┌┬┐"
        elif styles == "pipes":
            self.animation = "┃┃┃┃┃┃┃┃┃"
        elif styles == "dots2":
            self.animation = "⣾⣽⣻⢿⡿⣟⣯⣷"
        elif styles == "dots3":
            self.animation = "⢄⢂⢁⡁⡈⡐⡠"
        elif styles == "stars":
            self.animation = "✶✸✹✺✹✷"
        elif styles == "ping":
            self.animation = "⚫⚪"

    def __enter__(self):
        self.timer.enter()
        self.is_running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()
        return self

    def _animate(self):
        while self.is_running:
            self.say.say(f"\r{self.message} {self.animation[self.index]}", color=self.color)
            time.sleep(0.1)
            self.index = (self.index + 1) % len(self.animation)

    def __exit__(self, exc_type, exc_value, traceback):
        self.is_running = False
        self.thread.join()
        clear = " " * (len(self.message) + len(self.animation) + 1)
        print(f"\r{clear}\r", end="", flush=True)
        self.timer.exit()

#==============================================================================#

class Timer:
    """Measures and prints the execution time of a task."""

    def __init__(self, message: str = "Task"):
        """
        Initializes the TaskTimer object.

        Args:
            message (str, optional): A descriptive message to display (default: "Task").
        """
        self.say = Text()
        self.message = message

    def enter(self):
        """Starts the timer."""
        self.start_time = time.time()
        return self

    def exit(self):
        """Ends the timer and prints the execution time."""
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        message = f"{self.message} completed in {elapsed_time:.2f} seconds."
        self.say.say(message, color="green", bold=True)
    
    def end(self):
        """Ends the timer."""
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        message = f"{self.message} completed in {elapsed_time:.2f} seconds."
        self.say.say(message, color="green", bold=True)

if __name__ == "__main__":
    
    status = Status(styles="blocks")
    timer = Timer()

    with status:
        timer.enter()
        time.sleep(2)
        timer.exit()