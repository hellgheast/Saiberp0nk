from random import randint
from typing import Tuple
from evennia import set_trace
from enum import IntEnum
from module.enums import Stat,Skill,SaveThrow

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
    

    def rollWithModifier(self,rollString:str,modifier:int):
        return self.roll(rollString) + modifier
    
    def skillCheck(self,character,stat:Stat,skill:Skill,target:int) -> bool:
        roll = self.roll("2d6")
        skillValue = character.traits[skill.value].value
        statValue = character.traits[stat.value].value
        
        result = roll + skillValue + statValue
        
        if result >= target:
            return True
        else:
            return False

    def opposedSkillCheck(self,character,opponent,charSkill:Skill,opponentSkill:Skill) -> bool:
        if charSkill is None:
            resultChar = self.roll("2d6")
        else:
            resultChar = self.roll("2d6") + character.traits[charSkill.value].value
        
        if opponentSkill is None:
            resultOpponent = self.roll("2d6")
        else:
            resultOpponent = self.roll("2d6") + opponent.traits[charSkill.value].value

        if resultChar >= resultOpponent:
            return True
        else:
            return False


    def savingThrow(self, character,type:SaveThrow,target:int):
        match type:
            case SaveThrow.PHYSAVE:
                sub = max(character.traits[str(Stat.FOR)].mod,character.traits[str(Stat.CON)].mod)
            case SaveThrow.EVSAVE:
                sub = max(character.traits[str(Stat.INT)].mod,character.traits[str(Stat.DEX)].mod)
            case SaveThrow.MENTSAVE:
                sub = max(character.traits[str(Stat.FOR)].mod,character.traits[str(Stat.CON)].mod)
            case SaveThrow.LUCKSSAVE:
                sub = 0

        roll = self.roll("1d20")

        if roll == 20:
            return True
        elif roll == 1:
            return False
        else:        
            return roll >= target - sub

    def rollRandomTable(self,dieRoll,tableChoices):
        
        rollResult = self.roll(dieRoll)
        if isinstance(tableChoices[0],(tuple,list)):
            for valRange,choice in tableChoices:
                minval,*maxval = valRange.split("-",1)
                minval = abs(int(minval))
                maxval = abs(int(maxval[0]) if maxval else minval)
                
                if minval <= rollResult <= maxval:
                    return choice 
                
            # if we get here we must have set a dieroll producing a value 
            # outside of the table boundaries - raise error
            raise RuntimeError("rollRandomTable: Invalid die roll")
        else:
            # a simple regular list
            rollResult = max(1, min(len(tableChoices), rollResult))
            return tableChoices[rollResult - 1]
    
    #todo: combat roll


    def rollDeath(self,character):
        damageTable = (
            ("1","instantDeath"),
            ("2","internalDamage"),
            ("3","brainDamage"),
            ("4","eyeDamage"),
            ("5","gutWound"),
            ("6","rightLegRuined"),
            ("7","leftLegRuined"),
            ("8","rightArmRuined"),
            ("9","leftArmRuined"),
            ("10","systemDamage"),
            ("11-12","justFleshWound"),   
        )
        
        notLastingInjury = self.savingThrow(character,SaveThrow.PHYSAVE,16)
        if notLastingInjury == True:
            character.msg("Aucun dégâts long terme, simplement dans le coma..")
        else:
            damageType = self.rollRandomTable("1d12",damageTable)
            if damageType == "instantDeath":
                character.msg("You're dead !")
                character.atDeath()
            elif damageType == "justFleshWound":
                character.msg("You're fine")
            else:
                character.msg("Pas encore implémenté !")


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
#todo:refactor
def characterDefense(character):
    character.traits.DEF.base = 7 + character.traits.SAG.value
#todo:refactor
def acquireSkill(character,skill_id:str):
    #set_trace()
    if character.traits[skill_id] is None:
        raise Exception("Non existent skill")
    character.traits[skill_id].acquired = True
    character.traits[skill_id].base = 0
    character.traits[skill_id].mod = 0