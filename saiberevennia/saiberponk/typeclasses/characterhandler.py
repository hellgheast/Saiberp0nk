from module.enums import CombatMixin,Stat
from typing import Any
from enum import StrEnum


class CharacterHandler:
    """
    Helper handler to handle computed properties
    """

    ALLOWED_ATTRIBUTES = CombatMixin.attributes()

    def __init__(self, character) -> None:
        self.character = character
        if not character.db.data:
            character.db.data = {}
        self.data = character.db.data

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in CharacterHandler.ALLOWED_ATTRIBUTES:
            if __name == str(CombatMixin.PV):
                self.pv = __value
            else:
                self.data[__name] = __value
        else:
            super(CharacterHandler, self).__setattr__(__name, __value)

    def __setitem__(self, key, value) -> None:
        if key in CharacterHandler.ALLOWED_ATTRIBUTES:
            self.data[key] = value
        else:  
            Exception("Not existing")

    def __getattr__(self, name):
        if name not in self.data.keys():
            raise AttributeError
        return self.data.get(name, None)
    
    def __getitem__(self,name):
        if isinstance(name,StrEnum):
            name = str(name)
        if name not in self.data.keys():
            raise AttributeError
        if name == str(CombatMixin.MAXPV):
            self.maxPV
        return self.data.get(name, None)

    @property
    def maxPV(self):
        con = self.character.traits[Stat.CON].value
        currentPV = self.data.get(CombatMixin.PV,20)
        maxPV = 7 + con
        self.data[CombatMixin.MAXPV] = maxPV
        if currentPV > maxPV:
            self.data[CombatMixin.PV] = maxPV
        return maxPV


    @property
    def pv(self):
        return self.data.get(CombatMixin.PV,20)
    
    @pv.setter
    def pv(self,amount:int):
        maxPV = self.character.helper[CombatMixin.MAXPV]
        if amount > maxPV:
            self.character.msg("oups !")
        self.data[CombatMixin.PV] = amount



    
    
