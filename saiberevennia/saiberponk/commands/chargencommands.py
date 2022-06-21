from commands.command import Command
from evennia import CmdSet
import evennia
from evennia import set_trace,default_cmds

class CmdSetStr(Command):
    """
    Set the strength of a char

    Usage:
        setstrength <0-7>
    """
    key = "setstr"
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
        self.caller.db.strength = strength
        self.caller.msg("Your strength was set to %i." % strength)


class CharGenCmdSet(CmdSet):
    """Set de commandes pour la génération de personnage"""
    
    key = "CharGen"
    def at_cmdset_creation(self):
        self.add(CmdSetStr)
