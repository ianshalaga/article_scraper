from termcolor import colored
from functools import partial


def colored_print(text: str, color: str) -> None:
    """
        Prints text in console with color using termcolor library.

        Args:
        - text (str): Text to print in console.
        - color (str): Color for the text.

        Returns:
        - None
    """
    ctext = colored(text, color, attrs=["bold"])
    print(ctext)


# colored_print function wrappers
cprint_success = partial(colored_print, color="green")
cprint_warning = partial(colored_print, color="yellow")
cprint_failure = partial(colored_print, color="red")
cprint_info = partial(colored_print, color="blue")
