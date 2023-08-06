"""Run ChillBoss as a module."""

import click
from pyfiglet import figlet_format

from chillboss.mouse import Pointer
from chillboss import __version__


@click.command()
@click.option(
    "--movement",
    type=click.Choice(["random", "square"], case_sensitive=False),
    default="random",
    help="type of movement of mouse pointer.",
)
@click.option(
    "--length",
    type=int,
    default=None,
    help="custom length of the side of square during square movement.",
)
@click.option(
    "--sleeptime",
    type=int,
    default=30,
    help="amount of sleep time till next movement.",
)
@click.option(
    "--motiontime",
    type=int,
    default=0,
    help="amount of sleep time till next movement.",
)
def chill(motiontime, sleeptime, length, movement):
    """Start the movement of the mouse with the command line arguments passed by the user."""
    pointer = Pointer(
        movement=movement, length=length, sleep_time=sleeptime, motion_time=motiontime
    )
    print(figlet_format("ChillBoss"))
    print(f"Version: {__version__}")
    pointer.move_the_mouse_pointer()


if __name__ == "__main__":
    chill()
