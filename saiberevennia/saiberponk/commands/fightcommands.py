from commands.command import Command
from evennia import CmdSet
import random
from evennia import set_trace,default_cmds
from typeclasses.objects import SbWeaponBareHands

class CmdHit(Command):
    """
    Commmande de test pour frapper
    Usage:
        frapper <cible>
        frapper <cible> <arme>
        frapper <cible> avec <arme>

    """
    key = "frapper"
    help_category = "fight"

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
        caller = self.caller
        if not self.args:
            self.caller.msg("Qui veux-tu frapper ?")
            return
        target = self.caller.search(self.target)
        if not target:
            self.caller.msg("Cible inexistante..")
            return
        weapon = None
        # Use the equipement handler for using the weapons
        if self.weapon:
            weapon = self.caller.search(self.weapon)
        if weapon:
            weaponstr = f"{weapon.key}"
        else:
            weapon = SbWeaponBareHands.getBareHands()
            weaponstr = "poings"

        self.caller.msg(f"Tu frappes {target.key} à pleine puissance avec {weaponstr} !")
        target.msg(f"Tu te fais frapper par {self.caller.key} à pleine puissance avec {weaponstr} !")
        #TODO:Fix with poings
        weapon.use(caller,target)

        # announce
        message = f"{caller.key} frappe {target.key} avec {weaponstr}!"
        caller.location.msg_contents(message,
                                     exclude=caller)

class FightCmdSet(CmdSet):
    """Set de commandes pour le combat"""

    key = "fight"
    def at_cmdset_creation(self):
        self.add(CmdHit)