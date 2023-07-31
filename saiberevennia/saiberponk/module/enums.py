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

    @classmethod
    def enumList(cls) -> List[Enum]:
        return [x for x in cls]


class Stat(ExtEnum):
    FOR = "Force"
    INT = "Intelligence"
    SAG = "Sagesse"
    DEX = "Dextérité"
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
    # Fight Skills
    TIR = "Tirer"
    CAC = "Corps à corps"
    FRP = "Frapper"


class CombatMixin(ExtEnum):

    PV = "Points de vie"
    MAXPV = "Points de vie Max"
    DEF = "Défense"
    ATKBONUS = "Bonus d'attaque"
    RGARMORCLASS = "Classe d'armure/Distance"
    CQDARMORCLASS = "Classe d'armure/Corps à corps"

class SaveThrow(ExtEnum):
    PHYSAVE = "PHYSICAL"
    EVSAVE = "EVASION"
    MENTSAVE = "MENTAL"
    LUCKSSAVE = "LUCK"

class CharInfo(ExtEnum):
    BACKGROUND = "BACKGROUND"
    FIRSTNAME = "FIRSTNAME"
    LASTNAME = "LASTNAME"
    AGE = "AGE"
    HEIGHT = "HEIGHT"
    WEIGHT = "WEIGHT"


class WeaponType(ExtEnum):
    RANGED = "Distance"
    CLOSEQUARTER = "Corps à corps"


class MetaChoice(Enum):
    ANY_SKILL = Skill.enumList()
    ANY_STAT = Stat.enumList()
    ANY_COMBAT = [Skill.TIR,Skill.CAC,Skill.FRP]
    PHYSICAL = [Stat.CON, Stat.FOR, Stat.DEX]
    MENTAL = [Stat.CHA, Stat.INT, Stat.SAG]

    @classmethod
    def MetaChoice2str(cls,mc) -> str:
        match mc:
            case cls.ANY_SKILL:
                return "Toute compétence"
            case cls.ANY_STAT:
                return "Toute statistique"
            case cls.ANY_COMBAT:
                return "Combat (TIR,CAC,FRP)"
            case cls.PHYSICAL:
                return "Physiques (CON,FOR,DEX)"
            case cls.MENTAL:
                return "Mentales (CHA,INT,SAG)"
            
           

class Backgrounds(Enum):

    def __init__(
        self,
        desc: str,
        freeSkill: Skill,
        growth: List[MetaChoice | Skill | Stat],
        learning: List[Skill | MetaChoice],
    ) -> None:
        self.desc = desc
        self.freeSkill = freeSkill
        self.growth = growth
        self.learning = learning
    
    @classmethod
    def enumList(cls) -> List[Enum]:
        return [x for x in cls]

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
        ],
    )


class WieldLocation(ExtEnum):
    BACKPACK = "Sac à dos"
    LEFT_HAND = "Main gauche"
    RIGHT_HAND = "Main droite"
    TWO_HANDS = "Deux mains"
    BODY = "Corps"
    LEGS = "Jambes"
    HEAD = "Tête"

class ObjType(ExtEnum):
    WEAPON = "Arme"
    ARMOR = "Armure"
    HELMET = "Casque"
    CONSUMABLE = "Consommable"
    GEAR = "Équipement"
    QUEST = "Quête"
    CREDITUBE = "Créditube"

