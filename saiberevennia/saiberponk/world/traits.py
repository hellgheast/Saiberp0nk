from evennia.contrib.rpg.traits import StaticTrait,TraitHandler
from enum import StrEnum

class ExtTraitHandler(TraitHandler):
    """
    TraitHandler with modifications for direct access to traits through enums
    """

    def __getitem__(self, trait_key):
        """Returns `Trait` instances accessed as dict keys.
        If an StrEnum is passed the enum is converted into a string"""
        if isinstance(trait_key,StrEnum):
            trait_key = str(trait_key)
        return self.get(trait_key)

    
class SkillTrait(StaticTrait):

    """
    Skill Trait. This is a single value with a modifier,
    multiplier, and no concept of a 'current' value or min/max etc.

    We added the acquired value to indicate if this skill has been purchased or not

    value = (base + mod) * mult

    """
    trait_type = "skill"
    default_keys = {
        "base": 0, 
        "mod": -1, 
        "mult": 1.0,
        "acquired":False
    }    

    NOT_ACQUIRED_SKILL_VALUE = -1

    def __str__(self):
        status = "{value:11}".format(value=self.value)
        return "{name:12} {status} ({mod:+3}) (* {mult:.2f})/ acquired: {acq}".format(
            name=self.name, status=status, mod=self.mod, mult=self.mult,acq=self.acquired
        )

    # Helpers
    @property
    def acquired(self):
        return self._data["acquired"]
    
    @acquired.setter
    def acquired(self,boolean):
        if type(boolean) is bool:
            self._data["acquired"] = boolean
            # If it's not acquired put the not acquired modifier
            if self._data["acquired"] == False:
                self.mod = self.NOT_ACQUIRED_SKILL_VALUE
            if self._data["acquired"] == True:
                self.mod = 0
    
    @acquired.deleter
    def acquired(self):
        self._data["acquired"] = False

    @property
    def value(self):
        "The value of the Trait."
        return (self.base + self.mod) * self.mult


class StatTrait(StaticTrait):
    """
    Stat Trait. This is a single value with a modifier,
    multiplier, and no concept of a 'current' value or min/max etc.

    We modify the modifier depending on the base value

    value = (base) * mult

    """
    trait_type = "stat"
    default_keys = {
        "base": 0, 
        "mod": 0, 
        "mult": 1.0,
    }    


    def __str__(self):
        status = "{value:11}".format(value=self.value)
        return "{name:12} ({mod:+3}) (* {mult:.2f})".format(
            name=self.name,  mod=self.mod, mult=self.mult
        )


    # Helpers
    @property
    def base(self):
        return self._data["base"]

    @base.setter
    def base(self,value:int):
        if type(value) is int:
            self._data["base"] = value
            if value <= 3:
                self._data["mod"] = -2
            elif value >= 4 and value <= 7:
                self._data["mod"] = -1
            elif value >= 8 and value <= 13:
                self._data["mod"] = 0
            elif value >= 14 and value <= 17:
                self._data["mod"] = 1
            elif value >= 18:
                self._data["mod"] = 2

    @property
    def value(self):
        "The value of the Trait."
        return self.base * self.mult

# computedtrait,char=self,traits=["","",""],computefunc=..
# traitwithhook ??