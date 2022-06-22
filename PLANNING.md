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

