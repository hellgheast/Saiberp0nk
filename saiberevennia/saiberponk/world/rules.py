from random import randint
from typing import Tuple

def rollD6():
    return randint(1,6)

def roll3D6() -> Tuple[int,int,int]:
    return rollD6(),rollD6(),rollD6()

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


def rollSkillCheck(character,skill):
    pass