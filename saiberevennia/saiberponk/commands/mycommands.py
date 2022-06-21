from commands.command import Command
from evennia import CmdSet
import evennia
from evennia import set_trace,default_cmds

class CmdEchelon(Command):
    """
    Commande de base pour appeller Echelon
    """
    key = "echelon"

    def func(self):
        self.caller.msg(f"Bonjour {self.caller.key} je suis Echelon 2 !")
        if self.args:
            self.caller.msg(f"Ordres\t: [{self.args}]")


class CmdMobAdd(Command):
    """
    Fonction pour rajouter un mob pour faire des essais
    """
    key = "mobadd"
    def parse(self):
        pass
    def func(self):
        evennia.create_object("typeclasses.monsters.ArachBot",key="ArachTest",location=self.caller.location)


class CmdPrendre(default_cmds.CmdGet):
    """
    Commande pour prendre des objets
    """
    key = "prendre"

    def func(self):
        super().func()
        self.caller.msg(str(self.caller.location.contents))


class CmdFindTerm(Command):
    """
    Commande pour trouver un terminal
    """
    key = "recherche_terminal"

    def func(self):
        comterm = self.caller.search("comterm")
        if not comterm:
            return
        else:
            self.caller.msg("Un comterm est disponible !")

class CustomCmdSet(CmdSet):
    """Set de commandes spéciales"""

    def at_cmdset_creation(self):
        self.add(CmdEchelon)
        self.add(CmdMobAdd)
        self.add(CmdFindTerm)