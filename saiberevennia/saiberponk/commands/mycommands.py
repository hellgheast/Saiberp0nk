from commands.command import Command
from evennia import CmdSet
import evennia
from evennia import set_trace, default_cmds
from world import rules
from module import cinematic

# Main commands for testing and debugging


class CmdEchelon(Command):
    """
    Commande de base pour appeller Echelon
    """

    key = "echelon"

    def func(self):

        if self.args:
            self.caller.msg(f"Ordres\t: [{self.args}]")
            if "traitre" in self.args:
                cinematic.sendArrayText(
                    self.caller,
                    [
                        ("|rEspèce de salopard !|n", 1),
                        ("|304Je vais envoyer les TacMercs à tes trousses !|n", 1),
                        ("|550Fais tes prières !!|n", 1),
                        (
                            "|n|rERREUR: |yUTILISATEUR NON EXISTANT|n //..//.. |rDÉCONNEXION!!|n\n",
                            2,
                        ),
                    ],
                )
        else:
            textList = [
                (f"|gBonjour {self.caller.key} je suis Echelon 2 !|n\n", 2),
                ("|g.", 1),
                ("|g.", 1),
                ("|g.", 1),
                ("|gDemande d'accès|n ... |rCODE ROUGE|n", 0),
                (".", 1),
                (".", 1),
                (".", 1),
                ("|bAccès accordé|n\n", 5),
            ]
            cinematic.sendArrayText(self.caller, textList)


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
        # from evennia import set_trace;set_trace()

        strength = target.traits.FOR.value
        dexterity = target.traits.DEX.value
        intelligence = target.traits.INT.value

        if None in (strength, dexterity, intelligence):
            # Attributes not defined
            self.caller.msg("Not a valid target!")
            return

        text = f"You diagnose {target} as having {strength} strength, {dexterity} dexterity and {intelligence} intelligence."
        prompt = f"{strength} STR, {dexterity} DEX, {intelligence} INT"

        self.caller.msg(text=text)
        self.caller.msg(prompt=prompt)


class CmdStatCheck(Command):
    """
    Debug command for StatCheck

    Usage:
        statcheck statName targetNumber

    """

    key = "statcheck"

    def parse(self):
        if not self.args:
            self.statName = None
            self.targetNumber = None
        else:
            statName, targetNumber = self.args.strip().split(" ")
            self.statName = statName
            self.targetNumber = int(targetNumber)

    def func(self):
        caller = self.caller

        if self.statName == None and self.targetNumber == None:
            caller.msg("Missing arguments")
            return

        result = rules.rollStatCheck(caller, self.statName, self.targetNumber, True)
        if result:
            caller.msg(f"{self.statName} ROLL SUCCESS")
        else:
            caller.msg(f"{self.statName} ROLL FAILURE")


class CustomCmdSet(CmdSet):
    """Set de commandes spéciales"""

    def at_cmdset_creation(self):
        self.add(CmdEchelon)
        self.add(CmdMobAdd)
        self.add(CmdFindTerm)
        self.add(CmdInfo)
        self.add(CmdStatCheck)
