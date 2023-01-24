from typing import Dict, List
from enum import Enum

class WorldUtils:

    STATS_DICT:Dict[str,str] = {
        "FOR":"Force",
        "INT":"Intelligence",
        "SAG":"Sagesse",
        "DEX":"Dexterité",
        "CON":"Constitution",
        "CHA":"Charisme",
    }

    SKILL_DICT:Dict[str,str] = {
        "ACR":"Acrobate",
        "FAC":"Face",
        "TEC":"Tech", 
        "NIN":"Ninja",
        "UNI":"Universitaire",
        "MED":"Medic",
        "HCK":"Hacker",
        "MCD":"Marchand",
        "CRP":"Corporate",
        "BIO":"Biochem",
        "FLC":"Flic",
        "GNG":"Ganger",
    }

    FIGHT_DICT:Dict[str,str] = {
        "TIR":"Tir",
        "CAC":"Corps à corps"
    }

    COMPUTED_PROP:Dict[str,str] = {
        "PV":"Points de vie",
        "DEF":"Défense"
    }
    
    class CharInfo(Enum):
        CULTURE = "CULTURE"
        FIRSTNAME = "FIRSTNAME"
        LASTNAME = "LASTNAME"
        AGE = "AGE"
        HEIGHT = "HEIGHT"
        WEIGHT = "WEIGHT"
        @classmethod
        def attributes(cls) -> List[str] :
            return [cls.CULTURE,cls.FIRSTNAME,cls.LASTNAME,cls.AGE,cls.HEIGHT,cls.WEIGHT]





