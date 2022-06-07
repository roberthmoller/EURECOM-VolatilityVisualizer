from re import search
from typing import Optional

from lib.file import File
from lib.formats import Extract
from lib.guessers.guesser import TypeGuess


class NameTypeGuess(TypeGuess):
    @classmethod
    def guess(cls, file: File) -> Optional[int]:
        sorted_l = map(lambda kp: kp[0], sorted(Extract.types.items(), key=lambda kp: kp[1].priority, reverse=True))
        for index, key in enumerate(sorted_l):
            if search(rf".*{key}.*", file.name):
                return index
