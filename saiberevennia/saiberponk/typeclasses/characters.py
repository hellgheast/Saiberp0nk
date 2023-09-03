"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter
from evennia.utils import lazy_property
from evennia.contrib.rpg.traits import TraitHandler
from evennia import logger,AttributeProperty
from world.traits import ExtTraitHandler

from typeclasses.charinfohandler import CharInfoHandler
from typeclasses.characterhandler import CharacterHandler
from typeclasses.wallethelper import WalletHelper
from typeclasses.inventoryhandler import InventoryHandler,InventoryError
from module.enums import Stat,Skill,CombatMixin
from world.rules import dice,setSkill

from .objects import ObjectParent

import random


class LivingMixin:
    isPC = False

    @lazy_property
    def traits(self):
        return ExtTraitHandler(self)

    @lazy_property
    def helper(self):
        return CharacterHandler(self)

    @property
    def lifeLevel(self) -> str:
        percent = max(0, min(100, 100 * (self.helper[CombatMixin.PV] / self.helper[CombatMixin.MAXPV])))
        if 95 < percent <= 100:
            return "|gEn bonne santée|n"
        elif 80 < percent <= 95:
            return "|gÉraflé|n"
        elif 60 < percent <= 80:
            return "|GMeurtri|n"
        elif 45 < percent <= 60:
            return "|ySouffrant|n"
        elif 30 < percent <= 45:
            return "|yBlessé|n"
        elif 15 < percent <= 30:
            return "|rLourdement blessé|n"
        elif 1 < percent <= 15:
            return "|rÀ deux doigts de la mort|n"
        elif percent == 0:
            return "|REffondré!|n"
    
    def heal(self,pv):
        damage = self.helper[CombatMixin.MAXPV] - self.helper[CombatMixin.PV] 
        # You cannot negatively heal
        if pv < 0:
            pv = 0
        healValue = min(damage,pv)
        #TODO: Check when effect on HP are done !
        self.helper[CombatMixin.PV] += healValue
    
    def atPay(self,amount:int) -> int:
        amount = min(self.wallet.content(),amount)
        self.wallet.decrement(amount)
        return amount
    
    def atAttacked(self,attacker,**kwargs):
        pass

    def atDamage(self,damage,attacker=None):
        if damage < 0:
            damage = 0
        self.msg("DMG {} {}".format(type(damage),damage))
        self.helper[CombatMixin.PV] -= damage

    def atDefeat(self):
        self.atDeath()

    def atDeath(self):
        pass

    def atDoLoot(self,looted):
        looted.atLooted()
    
    def atLooted(self,looter):
        maxAmount = dice.roll("1d10")
        stolen = self.atPay(maxAmount)
        looter.wallet.increment(stolen)


class Character(ObjectParent, DefaultCharacter,LivingMixin):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_post_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    isPc = True
    
    @lazy_property
    def wallet(self):
        return WalletHelper(self)

    @lazy_property
    def charinfo(self):
        return CharInfoHandler(self)

    @lazy_property
    def inventory(self):
        return InventoryHandler(self)

    def at_object_creation(self):
        
        # STATS
        # Traits are nice for this
        for stat in Stat.attributes():
            self.traits.add(stat,stat,trait_type="stat")
         
        # SKILLS
        for skill in Skill.attributes():
            self.traits.add(skill,skill,trait_type="skill")

        # PV,DEF,ATKBONUS,ARMORCLASS
        for mixin in CombatMixin.attributes():
            # Computed properties
            self.helper[mixin] = 0

        self.helper[CombatMixin.ATKBONUS] = 0
        self.helper[CombatMixin.CQDARMORCLASS] = 10
        self.helper[CombatMixin.RGARMORCLASS] = 10


        self.wallet.setup()


        # Default values for fun
        self.charinfo.age = random.randint(1,100)
        self.db.xp = 0
        self.db.level = 1


    def at_pre_object_receive(self,movedObject,sourceLocation,**kwargs):
        return self.inventory.validateSlotUsage(movedObject)

    def at_object_receive(self,movedObject,sourceLocation,**kwargs):
        try:

            self.inventory.add(movedObject)
        except InventoryError:
            logger.log_trace()
    
    def at_pre_object_leave(self, leaving_object, destination, **kwargs):
        return True

    def at_object_leave(self,movedObject,destination,**kwargs):
        #from evennia import set_trace;set_trace()
        return self.inventory.remove(movedObject)

    def atDefeat(self):
        #TODO: Add allowDeath property
        if self.location.attributes.get("allowDeath") == True:
            dice.rollDeath(self)
        else:
            self.location.msg_contents(
                "Tu t'effrondres sur place, battu mais vivant.",
                from_obj=self)
            self.heal(self.heal[CombatMixin.MAXPV])
    
    def atDeath(self):
        self.location.msg_contents(
            "Tu t'effrondres sur place, sentant l'étreinte de la mort.",
            from_obj=self) 



    def return_appearance(self, looker):
        """
        The return from this method is what
        looker sees when looking at this object.
        """
        #TODO: Refactor this method
        text = super().return_appearance(looker)
        text += self.inventory.displayLoadout()
        return text
    
class NPC(LivingMixin,DefaultCharacter):
    
    isPc = False

    hitDice = AttributeProperty(default=1, autocreate=False)
    armorClass = AttributeProperty(default=(10,10), autocreate=False)
    genericSkill = AttributeProperty(default=1, autocreate=False)
    saveTarget = AttributeProperty(default=15, autocreate=False)
    atkBonus = AttributeProperty(default=1, autocreate=False)
    dmg = AttributeProperty(default=1, autocreate=False)
    #traumaTarget = AttributeProperty(default=1, autocreate=False)
    #shock = AttributeProperty(default=1, autocreate=False)


    def at_object_creation(self):
        
        # STATS
        # Traits are nice for this
        for stat in Stat.attributes():
            self.traits.add(stat,stat,trait_type="stat")
            self.traits[stat].base = 8
         
        # SKILLS
        for skill in Skill.attributes():
            self.traits.add(skill,skill,trait_type="skill")
            setSkill(self,skill,self.genericSkill)

        # PV,DEF,ATKBONUS,ARMORCLASS
        for mixin in CombatMixin.attributes():
            # Computed properties
            self.helper[mixin] = 0
        
        self.helper[CombatMixin.MAXPV] = self.hitDice * 5
        self.helper[CombatMixin.PV] = self.hitDice * 5
        self.helper[CombatMixin.CQDARMORCLASS] = self.armorClass[0]
        self.helper[CombatMixin.RGARMORCLASS] = self.armorClass[1]
        self.helper[CombatMixin.ATKBONUS] = self.atkBonus




class Mob(NPC):
    pass