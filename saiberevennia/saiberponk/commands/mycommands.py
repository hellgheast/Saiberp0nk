from commands.command import Command
from evennia import CmdSet
import evennia
from evennia import set_trace, default_cmds


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
        evennia.create_object(
            "typeclasses.monsters.ArachBot",
            key="ArachTest",
            location=self.caller.location,
        )


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


class CmdInfo(Command):
    """
    Commande d'information sur ton personnage
    """

    key = "info"

    def func(self):
        if not self.args:
            target = self.caller
        else:
            target = self.search(self.args)
            if not target:
                return
        # try to get stats
        strength = target.db.strength
        dexterity = target.db.dexterity
        intelligence = target.db.intelligence

        if None in (strength, dexterity, intelligence):
            # Attributes not defined
            self.caller.msg("Not a valid target!")
            return

        text = f"You diagnose {target} as having {strength} strength, {dexterity} dexterity and {intelligence} intelligence."
        prompt = f"{strength} STR, {dexterity} DEX, {intelligence} INT"
        self.caller.msg(text, prompt=prompt)


class CustomCmdSet(CmdSet):
    """Set de commandes spéciales"""

    def at_cmdset_creation(self):
        self.add(CmdEchelon)
        self.add(CmdMobAdd)
        self.add(CmdFindTerm)
        self.add(CmdInfo)
