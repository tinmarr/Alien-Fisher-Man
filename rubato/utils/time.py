from typing import Callable
from pygame.time import Clock, get_ticks
from rubato.utils import classproperty


class Time:
    """
    A time class to monitor time and to call functions in the future.
    """
    clock = Clock()
    calls = {}

    @staticmethod
    def delta_time(form: str = "milli") -> int:
        """
        Gets the time since the last frame, in milliseconds.

        :param form: The format the output should be (sec, milli)
        :return: Time since the last frame, in the given form.
        """
        if form == "sec":
            return Time.milli_to_sec(Time.clock.get_time())
        elif form == "milli":
            return Time.clock.get_time()
        else:
            raise ValueError(f"Style {form} is not valid")

    @staticmethod
    def now() -> int:
        """
        Gets the time since the start of the game, in milliseconds.

        :return: Time since the start of the game, in milliseconds.
        """
        return get_ticks()

    @staticmethod
    def set(clock: "Clock"):
        """
        Allows you to set the clock object property to a Pygame Clock object.

        :param clock: A pygame Clock object.
        """
        Time.clock = clock

    @staticmethod
    def milli_to_sec(milli: int) -> float:
        """
        Converts milliseconds to seconds.

        :param milli: A number in milliseconds.
        :return: The converted number in seconds.
        """
        return milli / 1000

    @staticmethod
    def delayed_call(delta_time: int, func: Callable):
        """
        Calls the function func at a later time.

        :param delta_time: The time in milliseconds to run the function at.
        :param func: The function to call.
        """
        run_at = delta_time + Time.now()

        if Time.calls.get(run_at):
            Time.calls[run_at].append(func)
        else:
            Time.calls[run_at] = [func]

    @staticmethod
    def process_calls():
        """Processes the calls needed"""
        for call in sorted(Time.calls.keys()):
            if call <= Time.now():
                for func in Time.calls[call]:
                    func()
                del Time.calls[call]
            else:
                break
