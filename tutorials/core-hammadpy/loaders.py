from hammadpy.core import Core
import time

core = Core()
with core.status("Pretty loaders!!!!", color="red"):
    time.sleep(2)

with core.status("Yeah thats kinda it..", color="green"):
    time.sleep(2)

with core.status("Cool Styles!!!!", color="magenta", styles="blocks"):
    time.sleep(2)

with core.status("I like this one a lot", color="rgb(255, 0, 0)", styles="emoji"):
    time.sleep(2)

with core.status("But its cool!!", color="green", animation="you can use your own!"):
    time.sleep(2)