from hammadpy.core import Text
import time

text = Text()

text.say("Text Built with Rust!!!", bold=True)
time.sleep(0.5)

text.say("This is better print basically!", underline=True)
text.say("This is ITALIC!", italic=True)
text.say("This is blue", color="blue")
text.say("This is red", color="red")
text.say("This is red on blue", color="red", bg="blue")
text.say("This is also red on blue", color="red", bg="blue")
text.say("You can use RGB values too!", color="rgb(0, 255, 136)")
text.say("Background RGB truecolor also works :O", color="white", bg="rgb(135, 28, 167)")
text.say("You can also make bold comments", color="white", bold=True)
text.say("Or use any string type", color="cyan")
text.say("Or change advice. This is red", color="red")
text.say("Or clear things up. This is default color and style", color="red", bold=True)
text.say("Purple and magenta are the same", color="purple")
text.say("Bright colors are also allowed", color="bright_blue", bg="bright_white")
text.say("You can specify color by string", color="blue", bg="red")
text.say("And so are normal and clear", color="white")
text.say("This also works!", color="green", bold=True)
text.say("THIS IS EVERYTHING!", color="white", bg="red", bold=True, italic=True, underline=True)