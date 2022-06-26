from abc import ABC
from typing import List, Type, Optional

from lib.file import File


class CanGuess:
    @classmethod
    def guess(cls, file: File) -> Optional[int]:
        raise NotImplementedError


class TypeGuess(ABC, CanGuess):
    __default__ = 0
    __implementations__: List[Type[CanGuess]] = []

    def __init_subclass__(cls, **kwargs):
        cls.__implementations__.append(cls)

    @classmethod
    def of(cls, file: File) -> int:
        for guesser in cls.__implementations__:
            guess = guesser.guess(file)
            if guess is not None:
                return guess
        return cls.__default__
