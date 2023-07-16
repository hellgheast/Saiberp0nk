from module.utils import Stat

class StatsHandler:
    """
    Main stats of the character
    """
#TODO: REFACTOR WITH TRAIT HANDLING
    def __init__(self, character) -> None:
        self.character = character

    @property
    def force(self):
        return self.character.traits.FOR.value
    
    @property.setter
    def force(self,amount):
        self.character.traits[Stat.FOR].value = amount

    @property
    def dexterite(self):
        return self.character.db.dexterite
    
    @property.setter
    def dexterite(self,amount):
        self.character.db.dexterite = amount


    
    
