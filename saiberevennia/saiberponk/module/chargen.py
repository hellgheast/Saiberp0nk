from world.rules import dice
from typeclasses.charinfohandler import CharInfoHandler
from module.enums import Stat,Skill,CharInfo,CombatRelated
from typeclasses.characters import Character
from evennia import EvMenu



_TEMP_SHEET = """
Prénom : {firstname} Nom: {lastname}

FORCE :{FOR}
INTELLIGENCE:{INT}
SAGESSE:{SAG}
DEXTERITÉ:{DEX}
CONSTITUTION:{CON}
CHARISME:{CHA}

{desc}
"""


class tempCharSheet:

    def __init__(self) -> None:
        
        # Base stats
        self.stats = {stat:0 for stat in Stat.attributes()}
        # Skills
        self.skills = {skill:0 for skill in Skill.attributes()}
        # CharInfo
        self.charinfo = {ci:"" for ci in CharInfo.attributes()}
        # Description
        self.desc = "Zlatows, le super zlatis"
    
    def showSheet(self):
        return _TEMP_SHEET.format(
            firstname=self.charinfo[CharInfo.FIRSTNAME],
            lastname=self.charinfo[CharInfo.LASTNAME],
            FOR=self.stats[Stat.FOR],
            INT=self.stats[Stat.INT],
            SAG=self.stats[Stat.SAG],
            DEX=self.stats[Stat.DEX],
            CON=self.stats[Stat.CON],
            CHA=self.stats[Stat.CHA],
            desc=self.desc
        )

    def apply(self,char:Character):
        try:
            # Apply stats
            for stat,value in self.stats.items():
                char.traits[stat].base = value
            
            #TODO: Apply skills
        
            # Apply charinfo
            for key,info in self.charinfo.items():
                char.charinfo[key] = info
        except Exception as e:
            char.msg(f"{e}")


def nodeChargen(caller,rawString,**kwargs):
    
    caller.msg(f"{kwargs}")
    # Workaround as kwargs are not correctly tranmitted
    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar
    
    text = tmpChar.showSheet()
    
    options = [
        {
            "desc":"Changer ton nom",
            "goto":("nodeChangeName",kwargs)
        }
    ]
    options.append(
        {
            "desc":"Génération aléatoire de personnage",
            "goto":("nodeRollStat",kwargs)

        }
    )
    options.append(
        {
            "desc":"Accepter et créer ton personnage",
            "goto":("nodeApplyChargen",kwargs)
        },
    )

    return text,options


def _update_name(caller, rawString:str, **kwargs):
    """
    Used by node_change_name below to check what user 
    entered and update the name if appropriate.

    """
    if rawString:
        tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar
        tmpChar.charinfo[CharInfo.FIRSTNAME],tmpChar.charinfo[CharInfo.LASTNAME] = [x.lower().capitalize() for x in rawString.split(" ")]


    return "nodeChargen", kwargs


def nodeChangeName(caller, rawString:str, **kwargs):
    """
    Change the random name of the character.

    """
    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar

    text = (
        f"Ton nom actuel est |w{tmpChar.charinfo[CharInfo.FIRSTNAME]} {tmpChar.charinfo[CharInfo.LASTNAME]}|n. "
        "Enter a new name or leave empty to abort." 
    )

    options = {
                   "key": "_default", 
                   "goto": (_update_name, kwargs)
              }

    return text, options



def nodeRollStat(caller, rawString:str, **kwargs):


    caller.msg("Lancement des dés...")

    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar

    for stat in Stat.attributes():

        tmpChar.stats[stat]=dice.roll("3d6")
        caller.msg(f"{stat} = {tmpChar.stats[stat]}")
    
    text = (
        f"Génération alétoire de personnage"
    )
    
    options = [
        {
            "desc":"retour ?",
            "goto":("nodeChargen",kwargs)
        }
    ]

    return text,options


def nodeApplyChargen(caller, rawString:str, **kwargs):
    """                              
    End chargen and create the character. We will also puppet it.
                                     
    """                              
    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar
    tmpChar.apply(caller)      
    
    text = "Character created!"
    
    return text, None 

def startChargen(caller,session=None):
    """
    Starting point
    """
    caller.msg("BOUYA")
    menutree = {
        "nodeChargen":nodeChargen,
        "nodeChangeName":nodeChangeName,
        "nodeRollStat":nodeRollStat,
        "nodeApplyChargen":nodeApplyChargen
    }

    tmpChar = tempCharSheet()

    # Generate a template char
    EvMenu(caller,menutree,session=session,
           startnode="nodeChargen",tmpChar=tmpChar)
    caller.msg("BOUYO")