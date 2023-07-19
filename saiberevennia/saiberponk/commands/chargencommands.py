from commands.command import Command
from evennia import CmdSet,EvMenu
import evennia
from evennia import set_trace,default_cmds


from world import rules
from module.utils import Stat,Skill

class CmdSetStat(Command):
    """
    Set an Attribute of a char

    Usage:
        setStats <STAT> <1-20>
    """
    key = "setStat"
    help_category = "chargen"

    def parse(self):
        errmsg = "No arguments !"
        if not self.args:
            self.caller.msg(f"{errmsg}")
            return
        else:
            statName,statValue = self.args.strip().split(" ")
            self.statName = None
            self.statValue = None
            try:
                self.statValue = int(statValue)
                self.statName = Stat.reverseMap(statName)
            except ValueError:
                errmsg = "Value is not a number !"
                self.caller.msg(f"{errmsg}")
                return
            except KeyError:
                errmsg = "Attribute is not correct !"
                self.caller.msg(f"{errmsg}")
        
    
    def func(self):
        errmsg = "Error."
        if not self.args:
            self.caller.msg(errmsg)
            return
        if self.statName is None or self.statValue is None:
            errmsg = "Parse error"
            self.caller.msg(errmsg)
            return
        if not (1 <= self.statValue <= 20):
            errmsg = "Value should be between 1 and 20"
            self.caller.msg(errmsg)
            return
        # at this point the argument is tested as valid. Let's set it.
        self.caller.traits[self.statName].base = self.statValue
        self.caller.msg(f"Your {self.statName} was set to {self.statValue}.")

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
            self.skillName = None
            try:
                self.skillName = Skill.reverseMap(skillName)
            except KeyError:
                errmsg = "Skill is not correct !"
                self.caller.msg(f"{errmsg}")

    def func(self):
        caller = self.caller
        
        if self.showStats:
            caller.msg("Liste des compétences disponibles\n")
            for skill in Skill.attributes():
                if caller.traits[f"{skill}"].trait_type == "skill":
                    caller.msg(f"{Skill.shortNames(skill)}/{caller.traits[skill].name}\n")
            return
        else:
            if self.skillName is None:
                errmsg = "Skill is not correct !"
                self.caller.msg(f"{errmsg}")
                return
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


class CmdSelectBackground(Command):

    """
    Command to show the available background and proceed to the selection of it
    With the skill selection or randomness


    Usage:
        selectbackground

    """
    key = "selectbackground"
    help_category = "chargen"
    def parse(self):
        pass
        if not self.args:
            self.statName = None
            self.statValue = None
        else:
            statName,statValue = self.args.strip().split(" ")
            self.statName = statName
            self.statValue = int(statValue)    

    def func(self):
        pass
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
        self.add(CmdSetStat)
        self.add(CmdStatSet)
        self.add(CmdBuySkill)
