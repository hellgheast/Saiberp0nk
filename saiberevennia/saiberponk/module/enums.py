from typing import Dict, List
from enum import Enum, StrEnum, auto

class ExtEnum(StrEnum):
    """
    Main Enum class that provides useful helper functions
    """
    @classmethod
    def reverseMap(cls, str) -> str:
        return cls.__members__.get(str).value

    @classmethod
    def shortNames(cls, str) -> str:
        INV_DICT = {v.value: k for k, v in cls.__members__.items()}
        return INV_DICT.get(str)
    
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

class FightSkill(ExtEnum):

    TIR = "Tirer"
    CAC = "Corps à corps"
    FRP = "Frapper"


class CombatRelated(ExtEnum):

    PV = "Points de vie"
    DEF = "Défense"


class CharInfo(ExtEnum):
    CULTURE = "CULTURE"
    FIRSTNAME = "FIRSTNAME"
    LASTNAME = "LASTNAME"
    AGE = "AGE"
    HEIGHT = "HEIGHT"
    WEIGHT = "WEIGHT"



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


