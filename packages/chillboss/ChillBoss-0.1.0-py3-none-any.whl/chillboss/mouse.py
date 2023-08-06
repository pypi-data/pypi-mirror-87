"""Interact with Pointer"""


from typing import Tuple, Optional
from random import randrange
from time import sleep


import pyautogui


class Pointer:
    """Driver for mouse pointer movement."""

    def __init__(
        self,
        movement: str = "random",
        length: Optional[int] = None,
        sleep_time: int = 30,
        motion_time: int = 0,
    ):
        self._movement: str = movement
        self._sleep_time: int = sleep_time
        self._motion_time: int = motion_time
        self._x_pixels: int
        self._y_pixels: int
        self._x_pixels, self._y_pixels = pyautogui.size()
        smaller_dimension: int = min(self._x_pixels, self._y_pixels)
        self._length: int = length if length is not None else smaller_dimension // 10
        if self._length > smaller_dimension and movement == "square":
            raise ValueError(
                f"length provided {length} is greater than display dimension for square movement. Max allowed for the current display is {smaller_dimension-1}"
            )

    def _get_random_coordinates(self) -> Tuple[int, int]:
        random_x_pixel: int = randrange(start=0, stop=self._x_pixels)
        random_y_pixel: int = randrange(start=0, stop=self._y_pixels)
        return random_x_pixel, random_y_pixel

    def _get_square_coordinates(
        self,
    ) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        half_length: int = self._length // 2
        x_center: int = self._x_pixels // 2
        y_center: int = self._y_pixels // 2
        if (
            x_center + half_length >= self._x_pixels
            or y_center + half_length >= self._y_pixels
        ):
            raise ValueError("Pixels out of bound of the screen")
        return (
            (x_center - half_length, y_center - half_length),
            (x_center + half_length, y_center - half_length),
            (x_center + half_length, y_center + half_length),
            (x_center - half_length, y_center + half_length),
        )

    def _random_movement(self) -> None:
        while True:
            try:
                x_move_to: int
                y_move_to: int
                x_move_to, y_move_to = self._get_random_coordinates()
                pyautogui.moveTo(x=x_move_to, y=y_move_to, duration=self._motion_time)
                sleep(self._sleep_time)
            except KeyboardInterrupt:
                break

    def _squared_movement(self) -> None:
        corners = self._get_square_coordinates()
        while True:
            try:
                for corner in corners:
                    x_move_to: int
                    y_move_to: int
                    x_move_to, y_move_to = corner
                    pyautogui.moveTo(
                        x=x_move_to, y=y_move_to, duration=self._motion_time
                    )
                    sleep(self._sleep_time)
            except KeyboardInterrupt:
                break

    def move_the_mouse_pointer(self) -> None:
        """Adapter to call movement method accordingly."""
        try:
            {
                "random": self._random_movement,
                "square": self._squared_movement,
            }[self._movement]()
        except KeyError:
            print(
                f"No {self._movement} movement applicable"
            )  # TODO: Would be replaced with logging
            raise
