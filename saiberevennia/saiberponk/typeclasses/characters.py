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

from typeclasses.charinfohandler import CharInfoHandler
from typeclasses.wallethelper import WalletHelper

from .objects import ObjectParent

import random

class Character(ObjectParent, DefaultCharacter):
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

    @lazy_property
    def traits(self):
        return TraitHandler(self)
    
    @lazy_property
    def wallet(self):
        return WalletHelper(self)

    @lazy_property
    def charinfo(self):
        return CharInfoHandler(self)
    #@lazy_property
    #def stats(self):
    #    return StatsHandler(self)



    def at_object_creation(self):

        # Will need to refactor it if needed
        
        
        # STATS
        self.traits.add("force","Force",trait_type="static",base=0,mod=0)
        self.traits.add("dexterite","Dexterité",trait_type="static",base=0,mod=0)
        self.traits.add("constitution","Constitution",trait_type="static",base=0,mod=0)
        self.traits.add("intelligence","Intelligence",trait_type="static",base=0,mod=0)
        self.traits.add("sagesse","Sagesse",trait_type="static",base=0,mod=0)
        self.traits.add("charisme","Charisme",trait_type="static",base=0,mod=0)

        # SKILLS
        self.traits.add("acrobate","Acrobate",trait_type="skill",base=0,mod=0)
        self.traits.add("face","Face",trait_type="skill",base=0,mod=0)
        self.traits.add("tech","Tech",trait_type="skill",base=0,mod=0)
        self.traits.add("ninja","Ninja",trait_type="skill",base=0,mod=0)
        self.traits.add("universitaire","Universitaire",trait_type="skill",base=0,mod=0)
        self.traits.add("medic","Medic",trait_type="skill",base=0,mod=0)
        self.traits.add("hacker","Hacker",trait_type="skill",base=0,mod=0)
        self.traits.add("marchand","Marchand",trait_type="skill",base=0,mod=0)
        self.traits.add("corporate","Corporate",trait_type="skill",base=0,mod=0)
        self.traits.add("biochem","Biochem",trait_type="skill",base=0,mod=0)
        self.traits.add("flic","Flic",trait_type="skill",base=0,mod=0)
        self.traits.add("ganger","Ganger",trait_type="skill",base=0,mod=0)

        # FIGHT SKILLS
        self.traits.add("tir","Tir",trait_type="static",base=0,mod=0)
        self.traits.add("cac","Corps à corps",trait_type="static",base=0,mod=0)

        # Computed properties
        self.traits.add("pv","Points de vie",trait_type="counter",base=0,min=0,max=None)
        self.traits.add("defense","Défense",trait_type="static",base=0,mod=0)

        self.wallet.setup()

        self.charinfo.age = random.randint(1,100)

        self.db.xp = 0

       
    def get_stats(self):
        """
        Get the main stats of this character
        """
        statTuple = (self.traits.force.value,
                    self.traits.dexterite.value, 
                    self.traits.constitution.value,
                    self.traits.intelligence.value,
                    self.traits.sagesse.value,
                    self.traits.charisme.value
                    )
        return statTuple


    def return_appearance(self, looker):
        """
        The return from this method is what
        looker sees when looking at this object.
        """
        text = super().return_appearance(looker)
        cscore = " (combat score: %s)" % self.db.combat_score
        if "\n" in text:
            # text is multi-line, add score after first line
            first_line, rest = text.split("\n", 1)
            text = first_line + cscore + "\n" + rest
        else:
            # text is only one line; add score to end
            text += cscore
        return text