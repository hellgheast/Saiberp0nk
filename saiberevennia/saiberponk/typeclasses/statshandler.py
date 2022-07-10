class StatsHandler:
    """
    Main stats of the character
    """

    def __init__(self, character) -> None:
        self.character = character

    @property
    def force(self):
        return self.character.db.force
    
    @property.setter
    def force(self,amount):
        self.character.db.force = amount

    @property
    def dexterite(self):
        return self.character.db.dexterite
    
    @property.setter
    def dexterite(self,amount):
        self.character.db.dexterite = amount


    
    
