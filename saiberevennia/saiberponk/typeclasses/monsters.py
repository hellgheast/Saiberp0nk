# hellgheast mob file

from typeclasses.objects import Object

class Monster(Object):
    """It's the base class for any monster in the game"""
    
    def move_around(self):
        print(f"{self.key} se déplace !")


class ArachBot(Monster):
    """The smallest mob in the game !"""
    def move_around(self):
        super().move_around()
        print(f"{self.key} cliquette d'un air menaçant !")
    
    def attack(self):
        print(f"{self.key} envoie une décharge !")