from hammadpy import Core
import time

core = Core()

status = core.status
with status(message="Loading...") as status:
    time.sleep(2)
    pass

status = core.status
with status(message="Loading...", styles="emoji") as status:
    time.sleep(2)
    pass