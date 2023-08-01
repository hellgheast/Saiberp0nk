from commands.command import Command
from evennia import CmdSet
import evennia
from evennia import set_trace, default_cmds
from world import rules
from module import cinematic
from module.enums import Stat, CharInfo, CombatMixin,Skill
from evennia.utils.evform import EvForm
from evennia.utils.evtable import EvTable
from module.forms import EV_PC_SHEET_DICT
from textwrap import dedent

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
        caller = self.caller
        if not self.args:
            target = self.caller
        else:
            #FIXME: Broken research
            target = self.search(self.args)
            if not target:
                return
        # try to get stats
        # from evennia import set_trace;set_trace()




        form = EvForm(data=EV_PC_SHEET_DICT)
        genSkill = {k: [target.traits[k].value,target.traits[k].acquired] for k in Skill.attributes()}
        form.map(
            cells={
                1: target.charinfo[CharInfo.LASTNAME],
                2: target.charinfo[CharInfo.FIRSTNAME],
                3: target.charinfo[CharInfo.BACKGROUND],
                4: target.return_appearance(caller),
                5: target.traits[Stat.FOR].value,
                6: target.traits[Stat.INT].value,
                7: target.traits[Stat.SAG].value,
                8: target.traits[Stat.DEX].value,
                9: target.traits[Stat.CON].value,
                10: target.traits[Stat.CHA].value,
                11: target.helper[CombatMixin.PV],
                12: target.helper[CombatMixin.MAXPV],
            },
            tables={
                "A": EvTable(
                    "Compétence",
                    "Niveau",
                    "Acquis",
                    table=[
                        [x for x in genSkill.keys()],
                        [x[0] for x in genSkill.values()],
                        ["Oui " if x[1] else "Non" for x in genSkill.values()],
                    ],
                    border="incols",
                )
            },
        )
        self.caller.msg(text=str(form))        


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
