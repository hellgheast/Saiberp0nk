from typing import Dict, List
from enum import Enum,StrEnum,auto


class Stat(StrEnum):
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
        STATS_DICT:Dict[str,str] = {
            "FOR":"Force",
            "INT":"Intelligence",
            "SAG":"Sagesse",
            "DEX":"Dexterité",
            "CON":"Constitution",
            "CHA":"Charisme",
        }
        return STATS_DICT.get(str)


class Skill(StrEnum):
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
    
    #TODO: Unify both methods
    @classmethod
    def reverseMap(cls,str) -> str:
        SKILL_DICT:Dict[str,str] = {
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
        return SKILL_DICT.get(str)
    
    @classmethod
    def shortNames(cls,str) -> str:
        SKILL_DICT:Dict[str,str] = {
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
        INV_SKILL_DICT = {v: k for k, v in SKILL_DICT.items()}
        return INV_SKILL_DICT.get(str)



class FightSkill(StrEnum):
    TIR = "Tirer"
    CAC = "Corps à corps"
    FRP = "Frapper"

    @classmethod
    def attributes(cls) -> List[str]:
        return [str(x) for x in cls]
    
    @classmethod
    def reverseMap(cls,str) -> str:
        FIGHT_DICT:Dict[str,str] = {
        "TIR":"Tirer",
        "CAC":"Corps à corps",
        "FRP":"Frapper"
        }
        return FIGHT_DICT.get(str)
    

class CombatRelated(StrEnum):
    PV  = "Points de vie"
    DEF = "Défense"
    
    @classmethod
    def attributes(cls) -> List[str]:
        return [str(x) for x in cls]
    
    @classmethod
    def reverseMap(cls,str) -> str:
        COMPUTED_PROP:Dict[str,str] = {
            "PV":"Points de vie",
            "DEF":"Défense"
        }
        return COMPUTED_PROP.get(str)

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




