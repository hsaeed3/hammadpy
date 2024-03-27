from yosemite.core.modules.text import Text
from yosemite.core.modules.loaders import Status
import time
import threading

def main():
    text = Text()

    with Status(message="", styles="moons"):
        try:
            text.say("Yosemite", color="rgb(255, 165, 0)", bold=True)
            text.say("Hammad Saeed", color="rgb('128', '128', '128')", italic=True)
            text.say("0.0.x - Half Dome", color="rgb('128', '128', '128')", italic=True)
            time.sleep(25)
        except KeyboardInterrupt:
            exit()
        
if __name__ == "__main__":
    main()