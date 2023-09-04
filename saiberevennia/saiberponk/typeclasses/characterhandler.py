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
        #TODO: Check how clean is this solution with properties and items 
        if __name in CharacterHandler.ALLOWED_ATTRIBUTES:
            self.data[__name] = __value
        else:
            super(CharacterHandler, self).__setattr__(__name, __value)

    def __getattr__(self, name):
        if name not in CharacterHandler.ALLOWED_ATTRIBUTES:
            raise AttributeError
        return self.data.get(name, None)
    

    def __setitem__(self, key: str, value:Any) -> None:
        if isinstance(key,StrEnum):
            key = str(key)
        if key in CharacterHandler.ALLOWED_ATTRIBUTES:
            match key:
                case str(CombatMixin.PV):
                    self.pv = value
                case str(CombatMixin.CW):
                    self.cw = value
                case _:
                    self.data[key] = value
        else:
            raise AttributeError("Not existing")
            
    def __getitem__(self,key):
        if isinstance(key,StrEnum):
            key = str(key)
        if key in CharacterHandler.ALLOWED_ATTRIBUTES:
            match key:
                case str(CombatMixin.MAXPV):
                    self.maxPV
                case str(CombatMixin.MAXCW):
                    self.maxCW
                case _:
                    pass  
        return self.data.get(key, None)

## Computed properties and co !

    @property
    def maxCW(self):
        """ Compute the maximum weight you can have in kilos"""
        const = self.character.traits[Stat.CON].value
        force = self.character.traits[Stat.FOR].value
        computemaxCW = 10 + ((const + force)/2) * 5
        self.data[CombatMixin.MAXCW.value] = computemaxCW
        return computemaxCW
    
    @property
    def cw(self):
        """Current weight carried by char"""
        return self.data.get(CombatMixin.CW,0)

    @cw.setter
    def cw(self,amount:int):
        #from evennia import set_trace;set_trace()
        computemaxCW = self.character.helper[CombatMixin.MAXCW]
        if amount > computemaxCW:
            self.character.msg("oups CW !")
            amount = computemaxCW
        self.data[CombatMixin.CW.value] = amount

    @property
    def maxPV(self):
        # We compute the maxPV value for PC
        if self.character.isPc:
            con = self.character.traits[Stat.CON].value
            currentPV = self.data.get(CombatMixin.PV.value,20)
            maxPV = 7 + con
            self.data[CombatMixin.MAXPV.value] = maxPV
            if currentPV > maxPV:
                self.data[CombatMixin.PV.value] = maxPV
            return maxPV
        else:
           return self.data[CombatMixin.MAXPV.value]

    @maxPV.setter
    def maxPV(self,amount:int):
        # We can only set this value for NPC
        if self.character.isPc == False:
           self.data[CombatMixin.MAXPV.value] = amount
           return self.data[CombatMixin.MAXPV.value]

    @property
    def pv(self):
        """Current point de vie on the character"""
        return self.data.get(CombatMixin.PV.value,20)
    
    @pv.setter
    def pv(self,amount:int):
        maxPV = self.character.helper[CombatMixin.MAXPV]
        if amount > maxPV:
            self.character.msg("oups PV !")
            amount = maxPV
        self.data[CombatMixin.PV.value] = amount



    
    
