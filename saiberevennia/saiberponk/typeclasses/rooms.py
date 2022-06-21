"""
Room

Rooms are simple containers that has no location of their own.

"""

import random
from evennia.objects.objects import DefaultRoom
from .objects import ObjectParent
from commands.chargencommands import CharGenCmdSet
from evennia import TICKER_HANDLER

class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    pass

class ChargenRoom(Room):
    """
    This room class is used by character-generation rooms. It makes
    the CharGenCmdSet available.
    """
    def at_object_creation(self):
        "this is called only at first creation"
        self.cmdset.add(CharGenCmdSet, permanent=True)


EVENT_STRINGS = [
    "Un bruit étrange se fait entendre..",
    "Une bourrasque de |yvent vous |rforce à vous couvrir..",
    "|r Zartam |npasse un cigare au bec, le |ylance-|rflamme|n facile..",
    "|rZlatows |nest entrain de manger un |gKebabum Imperalis|n avec une sauce de la |rvile albion.."
]

class RandomRoom(Room):
    """This room class is used to show some random events to the player which is inside"""
    
    def at_object_creation(self):
        self.db.interval = random.randint(10, 20)
        TICKER_HANDLER.add(
            interval=self.db.interval, callback=self.update_event
        )
    
    def at_object_delete(self):
        TICKER_HANDLER.remove(self.db.interval,self.update_event)
        return super().at_object_delete()

    def update_event(self, *args, **kwargs):
        """
        Called by the tickerhandler at regular intervals. Even so, we
        only update 50% of the time, picking a random event
        The tickerhandler requires that this hook accepts
        any arguments and keyword arguments (hence the *args, **kwargs
        even though we don't actually use them in this example)
        """
        if random.random() < 0.5:
            # only update 50 % of the time
            self.msg_contents("|w%s|n" % random.choice(EVENT_STRINGS))
