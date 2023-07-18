from typing import Dict, List
from enum import Enum,StrEnum,auto


class Stat(StrEnum):
    # This is a private dictionnary not an enum number
    __STATS_DICT:Dict[str,str] = {
        "FOR":"Force",
        "INT":"Intelligence",
        "SAG":"Sagesse",
        "DEX":"Dexterité",
        "CON":"Constitution",
        "CHA":"Charisme",
    }

    FOR = "Force"
    INT = "Intelligence"
    SAG = "Sagesse"
    DEX = "Dexterité"
    CON = "Constitution"
    CHA = "Charisme"

    @classmethod
    def attributes(cls) -> List[str]:
        return [str(x) for x in cls]

    @classmethod
    def reverseMap(cls,str) -> str:
        return Stat.__STATS_DICT.get(str)
    
    @classmethod
    def shortNames(cls,str) -> str:
        INV_DICT = {v: k for k, v in Stat.__STATS_DICT.items()}
        return INV_DICT.get(str)


class Skill(StrEnum):
    # This is a private dictionnary not an enum number
    __SKILL_DICT:Dict[str,str] = {
            "ADM":"Administrer",
            "CNT":"Connecter",
            "CND":"Conduire", 
            "EXE":"Exercer",
            "REP":"Réparer",
            "SOI":"Soigner",
            "SAV":"Savoir",
            "DIR":"Diriger",
            "PRF":"Performer",
            "PRC":"Percevoir",
            "PRG":"Programmer",
            "PSD":"Persuader",
            "MCD":"Marchander",
            "TRV":"Travailler"
    }

    ADM = "Administrer"
    CNT = "Connecter"
    CND = "Conduire" 
    EXE = "Exercer"
    REP = "Réparer"
    SOI = "Soigner"
    SAV = "Savoir"
    DIR = "Diriger"
    PRF = "Performer"
    PRC = "Percevoir"
    PRG = "Programmer"
    PSD = "Persuader"
    MCD = "Marchander"
    TRV = "Travailler"
    
    @classmethod
    def attributes(cls) -> List[str]:
        return [str(x) for x in cls]
    
    @classmethod
    def reverseMap(cls,str) -> str:
        return Skill.__SKILL_DICT.get(str)
    
    @classmethod
    def shortNames(cls,str) -> str:
        INV_DICT = {v: k for k, v in Skill.__SKILL_DICT.items()}
        return INV_DICT.get(str)



class FightSkill(StrEnum):
    __FIGHT_DICT:Dict[str,str] = {
        "TIR":"Tirer",
        "CAC":"Corps à corps",
        "FRP":"Frapper"
    }

    TIR = "Tirer"
    CAC = "Corps à corps"
    FRP = "Frapper"

    @classmethod
    def attributes(cls) -> List[str]:
        return [str(x) for x in cls]
    
    @classmethod
    def reverseMap(cls,str) -> str:

        return FightSkill.__FIGHT_DICT.get(str)
    
    @classmethod
    def shortNames(cls,str) -> str:
        INV_DICT = {v: k for k, v in FightSkill.__FIGHT_DICT.items()}
        return INV_DICT.get(str)


class CombatRelated(StrEnum):
    __COMPUTED_PROP:Dict[str,str] = {
        "PV":"Points de vie",
        "DEF":"Défense"
    }

    PV  = "Points de vie"
    DEF = "Défense"
    
    @classmethod
    def attributes(cls) -> List[str]:
        return [str(x) for x in cls]
    
    @classmethod
    def reverseMap(cls,str) -> str:
        return CombatRelated.__COMPUTED_PROP.get(str)
    
    @classmethod
    def shortNames(cls,str) -> str:
        INV_DICT = {v: k for k, v in CombatRelated.__COMPUTED_PROP.items()}
        return INV_DICT.get(str)


class Backgrounds(Enum):
    def __init__(self,freeSkill:Skill|FightSkill,GrowthTable,LearningTable) -> None:
        pass

class WorldUtils:
    pass


#    SKILL_DICT:Dict[str,str] = {
#        "ACR":"Acrobate",
#        "FAC":"Face",
#        "TEC":"Tech", 
#        "NIN":"Ninja",
#        "UNI":"Universitaire",
#        "MED":"Medic",
#        "HCK":"Hacker",
#        "MCD":"Marchand",
#        "CRP":"Corporate",
#        "BIO":"Biochem",
#        "FLC":"Flic",
#        "GNG":"Ganger",
#    }






    


    class CharInfo(StrEnum):
        CULTURE = "CULTURE"
        FIRSTNAME = "FIRSTNAME"
        LASTNAME = "LASTNAME"
        AGE = "AGE"
        HEIGHT = "HEIGHT"
        WEIGHT = "WEIGHT"
        @classmethod
        def attributes(cls) -> List[str]:
            return [str(x) for x in cls]




