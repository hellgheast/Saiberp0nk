from typing import Any
from module.enums import CharInfo

class CharInfoHandler:
    """
    Main information of the character
    """

    ALLOWED_ATTRIBUTES = CharInfo.attributes()

    def __init__(self, character) -> None:
        self.character = character
        if not character.db.charinfo:
            character.db.charinfo = {}
        self.charinfo = character.db.charinfo

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in CharInfoHandler.ALLOWED_ATTRIBUTES:
            self.charinfo[__name] = __value
        else:
            
            super(CharInfoHandler, self).__setattr__(__name, __value)
            # Had weird behavior with self.character and self.charinfo
            #raise Exception("Attribute not allowed !")

    def __getattr__(self, name):
        if name not in self.charinfo.keys():
            raise AttributeError
        return self.charinfo.get(name, None)

    @property
    def fullname(self) -> str:
        return self.charinfo[CharInfo.FIRSTNAME] + " " + self.charinfo[CharInfo.LASTNAME]
