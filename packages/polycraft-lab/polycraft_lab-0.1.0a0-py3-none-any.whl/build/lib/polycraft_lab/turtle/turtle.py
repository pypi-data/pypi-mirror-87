import logging
from collections import namedtuple
from enum import Enum
from typing import Tuple, Union

from polycraft_lab.installation.client import PolycraftClient

log = logging.getLogger(__name__)

Vector = namedtuple('Vector', 'direction magnitude')


class Direction(Enum):
    FORWARD = 0
    LEFT = 1
    BACKWARD = 2
    RIGHT = 3


class GameTurtle:
    """A turtle that can be used to interact with the game"""

    def __init__(self, client: PolycraftClient):
        self._client = client

    def attack(self):
        """Perform a left click where the camera is currently pointing."""
        pass

    def interact(self, auto=False):
        """Perform a right click where the camera is currently pointing.

        Args:
            auto (bool): If true, perform an interact command on the nearest
            interactable object.
        """

    def change_camera(self, modifier):
        """Change the direction of the camera."""

    def rotate(self, direction: Direction, amount: int = 1):
        """Rotate the camera by increments of 90°.

        Args:
            direction (Direction): The direction
            amount (int): The number of times to rotate.
        """

    def move(self, direction: Union[Tuple[Direction, int], Vector],
             teleport: bool = False):
        """Move the player.

        This takes a vector input with either a magnitude and direction or set
        of coordinates to move to (X, Y, Z).
        """
        log.debug('Moving player')
