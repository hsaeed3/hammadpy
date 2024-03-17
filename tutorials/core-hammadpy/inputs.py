from hammadpy.core import Input, Dialog

input = Input()
input.confirm("Inputs are built using prompt_toolkit. Press Enter to continue.")

options = ["Red", "Green", "Blue"]
chosen_option = Dialog.asklist(message=f"Inputs be used dynamically. Please choose a color from {options}", choices=options)

input.confirm(f"Are you sure you want to choose {chosen_option}")

name = input.ask("You can also ask for input directly in the terminal! Please enter your name:")
input.choice(f"Hello {name}! You can also choose from a list of options straight in the CLI! Please choose from {options}", choices=options)


