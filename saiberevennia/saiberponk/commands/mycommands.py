from commands.command import Command
from evennia import CmdSet

class CmdEchelon(Command):
    """
    Commande de base pour appeller Echelon
    """
    key = "echelon"

    def func(self):
        self.caller.msg(f"Bonjour {self.caller.key} je suis Echelon 2 !")
        if self.args:
            self.caller.msg(f"Ordres\t: [{self.args}]")

class CmdHit(Command):
    """
    Commmande de test pour frapper
    Usage:
        frapper <cible>
        frapper <cible> <arme>
        frapper <cible> avec <arme>

    """
    key = "frapper"
    # Continue https://www.evennia.com/docs/1.0-dev/Howtos/Beginner-Tutorial/Part1/More-on-Commands.html
    def func(self):
        args = self.args.strip()
        if not args:
            self.caller.msg("Qui veux-tu frapper ?")
        # Find the target in the same location than the caller
        target = self.caller.search(args)
        if not target:
            self.caller.msg("Cible inexistante..")
            return
        self.caller.msg(f"Tu frappes {target.key} à pleine puissance !")
        target.msg(f"Tu te fais frapper par {self.caller.key} à pleine puissance !")


class CustomCmdSet(CmdSet):
    """Set de commandes spéciales"""

    def at_cmdset_creation(self):
        self.add(CmdEchelon)
        self.add(CmdHit)