from random import randint
from typing import Tuple
from evennia import set_trace
from enum import IntEnum
from module.enums import Stat,Skill

class Difficulty(IntEnum):
    EASY = 6
    MEDIUM = 8
    HARD = 10
    VERY_HARD = 12
    COMPLEX = 14

class RollEngine():
    """Main roll system for saiberponk"""

    def roll(self,rollString:str) -> int:
        """
        Transform a roll string i.e 4d6 into 4 random int and sum them
        """
        # Split arg
        numberRolls,dieSize = rollString.split("d")
        # Convert into int
        numberRolls = int(numberRolls)
        dieSize = int(dieSize)
        # Generate the rolls an
        rollSum = sum([randint(1,dieSize) for _ in range(numberRolls)])
        return rollSum
    
    def skillCheck(self,character,stat:Stat,skill:Skill,target:int) -> bool:
        roll = self.roll("2d6")
        skillValue = character.traits[skill.value].value
        statValue = character.traits[stat.value].value
        
        result = roll + skillValue + statValue
        
        if result >= target:
            return True
        else:
            return False


    def savingThrow(self, character,type:str,target:int):
        match type:
            case "PHYSICAL":
                sub = max(character.traits[str(Stat.FOR)].mod,character.traits[str(Stat.CON)].mod)
            case "EVASION":
                sub = max(character.traits[str(Stat.INT)].mod,character.traits[str(Stat.DEX)].mod)
            case "MENTAL":
                sub = max(character.traits[str(Stat.FOR)].mod,character.traits[str(Stat.CON)].mod)
            case "LUCK":
                sub = 0

        roll = self.roll("1d20")

        if roll == 20:
            return True
        elif roll == 1:
            return False
        else:        
            return roll >= target - sub


dice = RollEngine()


def rollD6():
    return randint(1,6)

def roll2D6() -> Tuple[int,int]:
    return rollD6(),rollD6()

def roll3D6() -> Tuple[int,int,int]:
    return rollD6(),rollD6(),rollD6()

#TODO: Add saveRoll in case of danger
#TODO: Add minimal system for opposing characters
#TODO: Add combat system implementation
# Turn by turn system
# Each opponent can do an ACTION (attack,use a skill,launch a thing) and 
# MANEUVER ( move from a few meter,hide,crouch,aim,reload,help, a manoeuver gives a bonus of +1 used with a an action)
# Initiative is calculated by INT roll, the higher the better

# Attack roll == Difficulty is equal to defense
# If hit it's FOR/DEX + combat dice for damages
# RISK AND PROWESS
# The player can once per turn chose a prowess and the system applies a flaw

def rollStatCheck(character,stat:str,targetNumber:int,debug=False) -> bool:
    """
    
    """

    # What happens if a traits doesn't exist ?
    if character.traits[stat] is None:
        raise Exception("stat not existing")

    charStat = character.traits[stat].value

    d1,d2,d3 = roll3D6()
    rollResult = charStat + d1 + d2 + d3
    
    if debug:
        character.msg("Stat roll check\n")
        character.msg(f"STAT: {character.traits[stat].name} / CHARSTAT: {charStat}\nTARGETVALUE: {targetNumber} / ROLLRESULT :{rollResult} = {charStat} + {d1+d2+d3}")

    if rollResult >= targetNumber:
        return True
    else:
        return False


# def characterMaxPv(character) -> float:
#     return 5 + 5 * character.traits.CON.base

# def updateMaxPv(character):
#     character.traits.PV.max = characterMaxPv(character)

# def setCurrentPv(character,amount):
#     character.traits.current.value = amount

def characterDefense(character):
    character.traits.DEF.base = 7 + character.traits.SAG.value

def acquireSkill(character,skill_id:str):
    #set_trace()
    if character.traits[skill_id] is None:
        raise Exception("Non existent skill")
    character.traits[skill_id].acquired = True
    character.traits[skill_id].base = 0
    character.traits[skill_id].mod = 0