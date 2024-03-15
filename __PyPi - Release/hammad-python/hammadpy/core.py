from hammadcore.modules.text import Text
from hammadcore.modules.loaders import Status, Timer

"""
hammadpy.core.core

The core module for the hammadpy package. Contains base hammadpy tools, and all
hammadpy-sm tools.

Example:
    core = Core()

Attributes:
    Core: A class for the core module.
"""

class Core:
    """
    A class for the core module.

    Attributes:
        text: A Text object for styling CLI output text.
    """
    def __init__(self):

        # Text Styling
        text = Text()
        self.art = text.splash
        self.say = text.say
        self.list = text.list

        # Loaders
        self.status = Status
        self.timer = Timer

        pass

if __name__ == "__main__":
    import time
    import random

    rgb = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    rgb2 = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    rgb = f"rgb{rgb}"
    rgb2 = f"rgb{rgb2}"

    core = Core()
    # Text Styling
    core.art(message="hammadpy", art="random", color=rgb)
    time.sleep(1)
    core.say("This has an underline!", underline=True)
    core.say("This is ITALIC!", italic=True)
    list_items = ["This is a list", "With some items", "And some colors"]
    core.list(list_items, color="blue", bg="white", bold=True)
    time.sleep(0.5)

    # Loaders
    with core.status(message="Loading...") as status:
        time.sleep(2)
        pass

    with core.status(styles="emoji", color="yellow") as status:
        time.sleep(2)
        pass

