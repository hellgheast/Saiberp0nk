# hellgheast mob file

from typeclasses.objects import Object

class Mob(Object):
    """It's the base class for any mob in the game"""
    
    def move_around(self):
        print(f"{self.key} se déplace !")


class ArachBot(Mob):
    """The smallest mob in the game !"""
    def move_around(self):
        super().move_around()
        print(f"{self.key} cliquette d'un air menaçant !")
    
    def attack(self):
        print(f"{self.key} envoie une décharge !")