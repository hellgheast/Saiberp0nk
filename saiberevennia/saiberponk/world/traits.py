from evennia.contrib.rpg.traits import StaticTrait

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
        "mod": -2, 
        "mult": 1.0,
        "acquired":False
    }    

    NOT_ACQUIRED_SKILL_VALUE = -2

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

    
    @acquired.deleter
    def acquired(self):
        self._data["acquired"] = False

    @property
    def value(self):
        "The value of the Trait."
        return (self.base + self.mod) * self.mult



# computedtrait,char=self,traits=["","",""],computefunc=..
# traitwithhook ??