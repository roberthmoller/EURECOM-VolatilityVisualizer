# from re import search
# from typing import Optional
#
# from lib.extract import Extract
# from lib.file import File
# from lib.guesser import TypeGuess
#
#
# class ContentTypeGuess(TypeGuess):
#     @classmethod
#     def guess(cls, file: File) -> Optional[int]:
#         content = file.read().decode('utf-8')
#         print('\n\nContentTypeGuess content\n', content)
#
