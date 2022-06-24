# Goal for minimal release

* Batch commands to build the world
* Character creation process
* Object system
* Simple but efficient Room description
* Support a small NPC
* World minimal description
* Dice roll
* RP/wear system
* Exchange system (money and object)
* Small quest (get X of Y)
* Action with objects (get/use/attack)
* Have a minimal XP system
* Custom intro screen
* Have minimal french support (own command set)

# As a user

* Being able to move 
* Being able to interact
* See own char stat.
* Being able to personalise my char

## Administration
* Game rules enforces by coded systems
* Out-of-character goes through specific channel and forum

## Building

* From external code and in-game commands if needed
* Building should be only be done by admin and GM

## System
* Based on nanochrome and customised
* Night and day follow an accelerated cycle
* Weather should change dynamically
* World economic system
* Influence/reputation system should be used
* Chars can be known by physical or name

## Rooms
* Main description
* Color codes
* Events can happen inside a room (flavor text)

## Objects/Items

* Objects will be created in stores
* Money is a account value and an item
* Multiples objects might stacks
* Object has a weight
* Object has status (broken or not) and could be repaired
* To find you should use a given weapon object
* Crafting should be part of the game
* NPC/Mobs have a state machine
* NPC and mobs differs -> Mobs are killable and the main interaction is fighting, NPC are killable and have multiples caracteristics
NPC should give quests

## Characters
* Only one active character at the time
* A player can have multiples character (would need MULTISESSION_MODE=2)
but only play one at the time -> override Account method
```python
def puppet_object(self, session, obj):
    if len(self.get_all_puppets()):
        self.msg("You're already playing a character.")
        return
    super().puppet_object(session, obj)
```
* Char-gen should be room and menu -> Need to change the DEFAULT_HOME
* Classes/Races are overloading the same object
* Hiding is based on perception
* Skill tree TBD
* XP should be given through RP/Game-action/Fight and working
* PvP will be allowed
* Clone based system, cost a lot and death can be definitive



### Sides-notes
* Have a look to contrib SdescHandler in the rpsystem contrib is nice and straightforward for having a handler example
* Handlers are good

basic explanation of a handler is:
1. a python object attached to a game object through a property
2. holds references to the object it is attached to, and to a cache (in our case, attributes) it is the sole manipulator of
3. holds methods for interacting with the cache and doing game actions
it's essentially a systems interface
one nice thing about handlers is you can use them as basically "this object is participating in the system"
you know that if the object has the handler, it also has all the methods necessary to interact with the system
as a result it lets you divest systems that exist across many object types so you don't have to build convoluted inheritance or lots of boilerplate
you just attach the handler in the creation method
and now you can do something like object.combat.attack(foo) and it Just Works™

```python

# Minimum handler
class CombatHandler(object):
    obj = None 
    
    def __init__(self, obj) -> None:
        self.obj = obj
# On the object you want the handler on
@lazy_property
    def combat(self) -> CombatHandler:
        return CombatHandler(self)
```


* To handle archetypes use a helper methed that would take the char and apply the desired archetype on it
i would do it with a helper method that applies the archetype traits and adds a cmdset for the archetype abilities
so you'd have a function set_archetype - not attached to a class, just in a module - and then you would pass the Character object and the desired archetype to it, e.g. set_archetype(char, "hacker")