from hammadpy import Core
import time

core = Core()

core.art("ART !!")
time.sleep(1)

core.art("COLOR !!", color="blue")
time.sleep(1)

core.art("RGB COLOR !!", color="rgb(220, 156, 200)")
time.sleep(1)

core.art("STYLES !!!!", art="dots")
time.sleep(1)
