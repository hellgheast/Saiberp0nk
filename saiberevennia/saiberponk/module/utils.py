from typing import Dict, List
from enum import Enum, StrEnum, auto


class ExtEnum(StrEnum):
    @classmethod
    def attributes(cls) -> List[str]:
        return [str(x) for x in cls]


class Stat(ExtEnum):
    FOR = "Force"
    INT = "Intelligence"
    SAG = "Sagesse"
    DEX = "Dexterité"
    CON = "Constitution"
    CHA = "Charisme"

    @classmethod
    def reverseMap(cls, str) -> str:
        return Stat.__members__.get(str).value

    @classmethod
    def shortNames(cls, str) -> str:
        INV_DICT = {v.value: k for k, v in Stat.__members__.items()}
        return INV_DICT.get(str)


class Skill(ExtEnum):
    ADM = "Administrer"
    CNT = "Connecter"
    CND = "Conduire"
    EXE = "Exercer"
    REP = "Réparer"
    SOI = "Soigner"
    SAV = "Savoir"
    DIR = "Diriger"
    PRF = "Performer"
    PCV = "Percevoir"
    PRG = "Programmer"
    INF = "Infiltrer"
    SRV = "Survivre"
    PSD = "Persuader"
    MCD = "Marchander"
    TRV = "Travailler"

    @classmethod
    def reverseMap(cls, str) -> str:
        return Skill.__members__.get(str).value

    @classmethod
    def shortNames(cls, str) -> str:
        INV_DICT = {v.value: k for k, v in Skill.__members__.items()}
        return INV_DICT.get(str)



class FightSkill(ExtEnum):
    __FIGHT_DICT: Dict[str, str] = {
        "TIR": "Tirer",
        "CAC": "Corps à corps",
        "FRP": "Frapper",
    }

    TIR = "Tirer"
    CAC = "Corps à corps"
    FRP = "Frapper"

    @classmethod
    def attributes(cls) -> List[str]:
        return [str(x) for x in cls]

    @classmethod
    def reverseMap(cls, str) -> str:

        return FightSkill.__FIGHT_DICT.get(str)

    @classmethod
    def shortNames(cls, str) -> str:
        INV_DICT = {v: k for k, v in FightSkill.__FIGHT_DICT.items()}
        return INV_DICT.get(str)


class CombatRelated(ExtEnum):
    __COMPUTED_PROP: Dict[str, str] = {"PV": "Points de vie", "DEF": "Défense"}

    PV = "Points de vie"
    DEF = "Défense"

    @classmethod
    def reverseMap(cls, str) -> str:
        return CombatRelated.__COMPUTED_PROP.get(str)

    @classmethod
    def shortNames(cls, str) -> str:
        INV_DICT = {v: k for k, v in CombatRelated.__COMPUTED_PROP.items()}
        return INV_DICT.get(str)


class MetaChoice(Enum):
    ANY_SKILL = [Skill.attributes(), FightSkill.attributes()]
    ANY_COMBAT = [FightSkill.attributes()]
    ANY_STAT = [Stat.attributes()]
    PHYSICAL = [Stat.CON.value, Stat.FOR.value, Stat.DEX.value]
    MENTAL = [Stat.CHA.value, Stat.INT.value, Stat.SAG.value]


class Backgrounds(Enum):

    def __init__(
        self,
        desc: str,
        freeSkill: Skill | FightSkill,
        growth: List[MetaChoice | Skill | Stat],
        learning: List[Skill | MetaChoice],
    ) -> None:
        self.desc = desc
        self.freeSkill = freeSkill
        self.growth = growth
        self.learning = learning


    BUM = (
        "Clodo",
        # free skill
        Skill.SRV,
        # Growth list
        [
            (1, MetaChoice.ANY_STAT),
            (2, MetaChoice.PHYSICAL),
            (2, MetaChoice.PHYSICAL),
            (2, MetaChoice.MENTAL),
            Skill.SRV,
            MetaChoice.ANY_SKILL,
        ],
        # Learning list
        [
            MetaChoice.ANY_COMBAT,
            Skill.SRV,
            Skill.CNT,
            Skill.INF,
            Skill.PCV,
            Skill.PSD,
            Skill.REP,
            Skill.MCD,
        ],
    )

    BUROCRAT = (
        "Fonctionnaire",
        # free skill
        Skill.ADM,
        # growth list
        [
            (1, MetaChoice.ANY_STAT),
            (2, MetaChoice.MENTAL),
            (2, MetaChoice.MENTAL),
            (2, MetaChoice.MENTAL),
            Skill.ADM,
            MetaChoice.ANY_SKILL,
        ],
        # learning list
        [
            Skill.ADM,
            Skill.SAV,
            Skill.PSD,
            Skill.PRG,
            Skill.DIR,
            Skill.MCD,
            Skill.PCV,
            MetaChoice.ANY_SKILL,
        ],
    )




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
