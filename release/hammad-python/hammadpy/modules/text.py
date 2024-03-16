import libhammadpy_text
from art import text2art

"""
hammadpy.core.text

This module provides a class for styling CLI output text. A wrapper on top of libhammadpy-text, a 
module built on rust.

Example:
    styles = Text()
    styles.say("This has an underline!", underline=True)
    styles.say("This is ITALIC!", italic=True)
    styles.say("This is blue", color="blue")
    styles.say("This is red", color="red")
    styles.say("This is red on blue", color="red", bg="blue")
    styles.say("This is also red on blue", color="red", bg="blue")
    styles.say("You can use RGB values too!", color="rgb(0, 255, 136)")
    styles.say("Background RGB truecolor also works :O", color="white", bg="rgb(135, 28, 167)")
    styles.say("You can also make bold comments", color="white", bold=True)
    styles.say("Or use any string type", color="cyan")
    styles.say("Or change advice. This is red", color="red")
    styles.say("Or clear things up. This is default color and style", color="red", bold=True)
    styles.say("Purple and magenta are the same", color="purple")
    styles.say("Bright colors are also allowed", color="bright_blue", bg="bright_white")
    styles.say("You can specify color by string", color="blue", bg="red")
    styles.say("And so are normal and clear", color="white")
    styles.say("This also works!", color="green", bold=True)

    padded_message = "Format works as expected. This will be padded".ljust(30)
    styles.say(padded_message, color="blue")

    truncated_message = "And this will be green but truncated to 3 chars"[:3]
    styles.say(truncated_message, color="green")

    list_items = ["This is a list", "With some items", "And some colors"]
    styles.list(list_items, color="blue", bg="white", bold=True)

Attributes:
    Text: A class for styling CLI output text.
"""

class Text:
    """
    A class for styling CLI output text.
    
    Attributes:
        say: A method to style and print a single line of text.
        list: A method to style and print a list of items.
    """
    def say(self, message, color="white", bg=None, bold=False, italic=False, underline=False):
        """
        Style and print a single line of text.

        Args:
            message (str): The message to be styled and printed.
            color (str, optional): The color of the text. Defaults to "white".
            bg (str, optional): The background color of the text. Defaults to None.
            bold (bool, optional): Whether the text should be bold. Defaults to False.
            italic (bool, optional): Whether the text should be italic. Defaults to False.
            underline (bool, optional): Whether the text should be underlined. Defaults to False.

        Returns:
            None
        """
        styled_message = libhammadpy_text.format_text(message, color, bg, bold, italic, underline)
        print(styled_message)

    def list(self, items, color="white", bg=None, bold=False, italic=False, underline=False):
        """
        Style and print a list of items.

        Args:
            items (list): The items to be styled and printed.
            color (str, optional): The color of the text. Defaults to "white".
            bg (str, optional): The background color of the text. Defaults to None.
            bold (bool, optional): Whether the text should be bold. Defaults to False.
            italic (bool, optional): Whether the text should be italic. Defaults to False.
            underline (bool, optional): Whether the text should be underlined. Defaults to False.

        Returns:
            None
        """
        styled_items = libhammadpy_text.format_list(items, color, bg, bold, italic, underline)
        for item in styled_items:
            print(item)

    def splash(self, message: str = "hammadpy", art: str = "random", color: str = "white", bg: str = None, bold: bool = False, italic: bool = False, underline: bool = False):
        """
        Creates an ASCII art styled Splash 'Logo' in the terminal.

        Args:
            message (str): The message to display in the splash.
            art (str): The ASCII art style to use.
            color (str): Text color (e.g., 'red', 'blue').
            bg (str): Background color (e.g., 'red', 'blue').
            bold (bool): Whether the text should be bold.
            italic (bool): Whether the text should be italic.
            underline (bool): Whether the text should be underlined.

        Returns:
            None
        """
        if art == "random":
            fonts = ["block", "caligraphy", "doh", "dohc", "doom", "epic", "fender", "graffiti", "isometric1", "isometric2", "isometric3", "isometric4", "letters", "alligator", "dotmatrix", "bubble", "bulbhead", "digital", "ivrit", "lean", "mini", "script", "shadow", "slant", "speed", "starwars", "stop", "thin", "3-d", "3x5", "5lineoblique", "acrobatic", "alligator2", "alligator3", "alphabet", "banner", "banner3-D", "banner3", "banner4", "barbwire", "basic", "bell", "big", "bigchief", "binary", "block", "broadway", "bubble", "caligraphy", "doh", "dohc", "doom", "dotmatrix", "drpepper", "epic", "fender", "graffiti", "isometric1", "isometric2", "isometric3", "isometric4", "letters", "alligator", "dotmatrix", "bubble", "bulbhead", "digital", "ivrit", "lean", "mini", "script", "shadow", "slant", "speed", "starwars", "stop", "thin"]
            import random
            art = random.choice(fonts)

        art_message = text2art(message, font=art)
        self.say(art_message, color=color, bg=bg, bold=bold, italic=italic, underline=underline)

if __name__ == "__main__":
    styles = Text()
    styles.say("This has an underline!", underline=True)
    styles.say("This is ITALIC!", italic=True)
    styles.say("This is blue", color="blue")
    styles.say("This is red", color="red")
    styles.say("This is red on blue", color="red", bg="blue")
    styles.say("This is also red on blue", color="red", bg="blue")
    styles.say("You can use RGB values too!", color="rgb(0, 255, 136)")
    styles.say("Background RGB truecolor also works :O", color="white", bg="rgb(135, 28, 167)")
    styles.say("You can also make bold comments", color="white", bold=True)
    styles.say("Or use any string type", color="cyan")
    styles.say("Or change advice. This is red", color="red")
    styles.say("Or clear things up. This is default color and style", color="red", bold=True)
    styles.say("Purple and magenta are the same", color="purple")
    styles.say("Bright colors are also allowed", color="bright_blue", bg="bright_white")
    styles.say("You can specify color by string", color="blue", bg="red")
    styles.say("And so are normal and clear", color="white")
    styles.say("This also works!", color="green", bold=True)

    padded_message = "Format works as expected. This will be padded".ljust(30)
    styles.say(padded_message, color="blue")

    truncated_message = "And this will be green but truncated to 3 chars"[:3]
    styles.say(truncated_message, color="green")

    list_items = ["This is a list", "With some items", "And some colors"]
    styles.list(list_items, color="blue", bg="white", bold=True)

    styles.splash("hammadpy", art="random", color="white")