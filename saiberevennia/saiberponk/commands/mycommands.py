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

    def parse(self):
        self.args = self.args.strip()
        # set_trace()
        target, *weapon = self.args.split(" avec ", 1)
        if not weapon:
            target, *weapon = self.args.split(" ", 1)
        self.target = target.strip()
        #TODO: Fix documentation
        # weapon is a list of a unique str
        if weapon:
            self.weapon = weapon[0].strip()
        else:
            self.weapon = None

    def func(self):
        if not self.args:
            self.caller.msg("Qui veux-tu frapper ?")
            return
        target = self.caller.search(self.target)
        if not target:
            self.caller.msg("Cible inexistante..")
            return
        weapon = None
        if self.weapon:
            weapon = self.caller.search(self.weapon)
        if weapon:
            weaponstr = f"{weapon.key}"
        else:
            weaponstr = "poings"

        self.caller.msg(f"Tu frappes {target.key} à pleine puissance avec {weaponstr} !")
        target.msg(f"Tu te fais frapper par {self.caller.key} à pleine puissance avec {weaponstr} !")


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
        self.add(CmdHit)
        self.add(CmdMobAdd)
        self.add(CmdFindTerm)