from commands.command import Command
from evennia import CmdSet
import evennia
from evennia import set_trace,default_cmds

from world import rules

class CmdSetForce(Command):
    """
    Set the strength of a char

    Usage:
        setForce <0-7>
    """
    key = "setForce"
    help_category = "chargen"

    def parse(self):
        return super().parse()
    
    def func(self):
        errmsg = "You must supply a number between 0 and 7."
        if not self.args:
            self.caller.msg(errmsg)
            return
        try:
            strength = int(self.args)
        except ValueError:
            self.caller.msg(errmsg)
            return
        if not (0 <= strength <= 7):
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.traits.force.base = strength
        self.caller.msg(f"Your strength was set to {strength}.")

class CmdBuySkill(Command):
    """
    Debug command for buying a skill

    Usage:
        buyskill skillname
        buyskill (show a list of available skills)
    """
    key = "buyskill"
    help_category = "chargen"

    def parse(self):
        if not self.args:
            self.showStats = True
        else:
            skillName = self.args.strip().split(" ")[0]
            self.showStats = False
            self.skillName = skillName

    def func(self):
        caller = self.caller
        
        if self.showStats:
            caller.msg("Liste des compétences disponibles\n")
            for trait in caller.traits.all:
                if caller.traits[f"{trait}"].trait_type == "skill":
                    caller.msg(f"{caller.traits[trait].name}\n")
            return
        else:
            #set_trace()
            rules.acquireSkill(caller,self.skillName)
            caller.msg(f"Compétence {self.skillName} achetée")


class CmdStatSet(Command):
    """
    Debug command for setting traits value


    Usage:
        statset statName statValue

    """
    key = "statset"
    help_category = "chargen"
    def parse(self):
        if not self.args:
            self.statName = None
            self.statValue = None
        else:
            statName,statValue = self.args.strip().split(" ")
            self.statName = statName
            self.statValue = int(statValue)    

    def func(self):
        caller = self.caller
        
        if self.statName == None and self.targetNumber == None:
            caller.msg("Missing arguments")
            return
        
        self.caller.traits[self.statName].base = self.statValue
        self.caller.msg(f"STAT {self.caller.traits[self.statName].name} set to value : {self.statValue}")


class CharGenCmdSet(CmdSet):
    """Set de commandes pour la génération de personnage"""
    
    key = "CharGen"
    def at_cmdset_creation(self):
        self.add(CmdSetForce)
        self.add(CmdStatSet)
        self.add(CmdBuySkill)
