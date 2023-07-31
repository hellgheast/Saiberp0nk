from world.rules import dice
from typeclasses.charinfohandler import CharInfoHandler
from module.enums import Stat,Skill,CharInfo,CombatMixin,Backgrounds,MetaChoice
from typeclasses.characters import Character
from typing import List
from evennia import EvMenu
from textwrap import dedent



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
        self.skills = {skill:[0,False] for skill in Skill.attributes()}
        # CharInfo
        self.charinfo = {ci:"" for ci in CharInfo.attributes()}
        # Description
        self.desc = "Zlatows, le super zlatis"

        # Stat array
        self.statArray:List[int] = [14,12,11,10,9,7]

        # Maximum number of skill you can buy
        self.maxSkillBuy = 2
    
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

    def resetStatAssignation(self):
        # Stat array
        self.statArray:List[int] = [14,12,11,10,9,7]
        # Base stats
        self.stats = {stat:0 for stat in Stat.attributes()}

    def apply(self,char:Character):
        try:
            # Apply stats
            for stat,value in self.stats.items():
                char.traits[stat].base = value
            
            #TODO: Apply skills
            for skill,value in self.skills.items():
                char.traits[skill].acquired = value[1]
                char.traits[skill].base = value[0]
            # Apply charinfo
            for key,info in self.charinfo.items():
                char.charinfo[key] = info
        except Exception as e:
            char.msg(f"{e}")


def nodeChargen(caller,rawString,**kwargs):
    
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
            "desc":"Génération de personnage",
            "goto":("nodeAssignStat",kwargs)

        }
    )
    options.append(
        {
            "desc":"Sélection d'origine",
            "goto":("nodeInfoBackgroundBase",kwargs)
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
            "desc":"retour au menu principal",
            "goto":("nodeChargen",kwargs)
        }
    ]

    return text,options


def _stat_assign_helper(caller,rawString:str,**kwargs):
    
    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar
    selectedStat = kwargs.get("stat",None)
    
    if rawString:
        value = int(rawString)
        if value in tmpChar.statArray:
            tmpChar.stats[selectedStat.value]=value
            tmpChar.statArray.remove(value)
            caller.msg(f"{selectedStat} = {value}")
    else:
        caller.msg("No assign")
    return "nodeAssignStat", kwargs

def subnodeAssignStatHelper(caller,rawString:str,**kwargs):

    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar
    selectedStat = kwargs.get("stat",None)
    showStr = "\t".join([str(x) for x in tmpChar.statArray])

    text = (
        f"Insérer la valeur pour {selectedStat.value}\nDisponible:\n{showStr}",
    )

    options = {
                "key": "_default", 
                "goto": (_stat_assign_helper, {"stat": selectedStat})
    }

    return text, options

def subnodeResetStat(caller,rawString:str,**kwargs):
    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar
    tmpChar.resetStatAssignation()
    return "nodeAssignStat", kwargs


def nodeAssignStat(caller,rawString:str,**kwargs):
    """
    Node to assign the stats
    """


    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar

    def _isAssigned(stat:Stat) -> str:
        nonlocal tmpChar
        if tmpChar.stats[stat] != 0:
            return "(x)"
        else:
            return ""


    showStr = "\t".join([str(x) for x in tmpChar.statArray])

    text = (
        f"Sélections des statistiques pour le personnage\n{showStr}",
    )
    
    options = [
        {
            "desc":"retour au menu",
            "goto":("nodeChargen",kwargs)
        },
    ]

    # Generate submenu assignation
    for stat in Stat.enumList():
        options.append(
            {
                "desc":f"Assigner {stat} {_isAssigned(stat)}",
                "goto":("subnodeAssignStatHelper",{"stat": stat})
            },
        )

    options.append(
        {
            "desc":"Reset des statistiques",
            "goto":(subnodeResetStat,kwargs)
        }
    )
    return text,options




#########################################################
#                 Informational Pages
#########################################################

# Thanks for Inspector Caracal for all the help
_BACKGROUND_INFO_DICT = {
    # The keys here are the different options you can choose, and the values are the info pages
    Backgrounds.BUM: dedent(
        """\
        Vagrant, junkie, wino... sometimes “homeless person” if somebody’s trying to coax donations. Most
        in your situation are treated as nothing more than human detritus one step away from a welcome
        grave. Maybe you were born to a poverty indistinguishable from professional indigence or maybe
        some event threw you down from a better life, but you don’t intend to go quietly.
        Being a societal castoff in a dystopia like this one is something only the strongest survive for long.
        With the skills you have,you mean to do far more than just survive.
        """
    ),
    Backgrounds.BUROCRAT: dedent(
        """\
        Somebody had to keep the wheels of government turning, and you were as good as any.
        The city governments may be little more than shells for corp exploitation, but they 
        and their army of functionaries keep the power on, the slums contained, and some pretense 
        of civic order in place. It can be a very lucrative line of work for those positioned to
        demand bribes and other inducement, but you're going to need to collect your bonus pay in a more
        direct fashion. You know how the machine works,and that can be worth more than any sum of bullets
        """
    ),
}


def nodeInfoBackgroundBase(caller,rawString:str,**kwargs):
    """Information générale avant la sélection d'un background particulier"""
    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar
    text = dedent(
        """\
        |wPage d'information|n
        Dans cette section vous allez choisir l'origine de votre personnage.
        Elle déterminera quel est vôtre vécu au sein de la ville ainsi que les compétences
        que vous avez au départ.    
    """
    )
    help = "Une chouette section avant le grand saut !"

    options = [
        {
            "desc":"retour au menu principal",
            "goto":("nodeChargen",kwargs)
        },
    ]

    # Generate submenu assignation
    for bg in _BACKGROUND_INFO_DICT.keys():
        options.append(
            {
                "desc":f"En savoir plus sur {bg.desc}",
                "goto":("nodeSelectBackground",{"chosenBackground": bg})
            },
        )

    return (text,help),options


def _showBackgroundSkill(bg:Backgrounds) -> str:
    """Fonction pour afficher correctement les compétences disponibles"""
    bgSheet:str = dedent(f"""
    Nom:{bg.desc}
    Compétence gratuite: {bg.freeSkill}
    """.strip()
    )
    
    learningSheet:str = "Compétences disponibles\n"
    for elem in bg.learning:
        if isinstance(elem,MetaChoice):
            learningSheet += "{}\n".format(MetaChoice.MetaChoice2str(elem))
        elif isinstance(elem,Skill):
            learningSheet += "{}\n".format(elem.value)
        else:
            # Show error
            learningSheet += "ERROR"
    completeStr = dedent(f"""
    {bgSheet}
    {15*"-"}
    {learningSheet}
    """)
    return completeStr


def nodeSelectBackground(caller,rawString:str, chosenBackground:Backgrounds=None,**kwargs):
    """Noeud d'information qui affiche les informations à propos de cette origine"""
    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar

    if not chosenBackground:
        return "no chosenBackground !"

    text = f"{_showBackgroundSkill(chosenBackground)} {_BACKGROUND_INFO_DICT[chosenBackground]}"
    help = f"Information concernant l'origine {chosenBackground.desc}"

    options = [
        {
            "desc":"retour au menu principal",
            "goto":("nodeChargen",kwargs)
        },
    ]
    options.append(
        {
            "desc":f"Devenir {chosenBackground.desc}",
            "goto":("subNodeBackground", {"chosenBackground":chosenBackground})
        }
    )

    # Generate submenu assignation
    for bg in _BACKGROUND_INFO_DICT.keys():
        if bg != chosenBackground:
            options.append(
                {
                    "desc":f"En savoir plus sur {bg.desc}",
                    "goto":("nodeSelectBackground",{"chosenBackground":bg})
                },
            )


    return (text, help), options


def subNodeBackground(caller, rawString:str,chosenBackground:Backgrounds=None,**kwargs):
    """Noeud de sélection qui permet la sélection des compétences de cette origine"""
    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar

    if not chosenBackground:
        return "no chosenBackground !"
    
    selected = [k for k,v in tmpChar.skills.items() if v[1] == True]
    
    options = [
        {
            "desc":"retour au menu principal",
            "goto":("nodeChargen",kwargs)
        },
    ]

    options.append(
        {
            "desc":"retour au menu de sélection des origines",
            "goto":("nodeInfoBackgroundBase",kwargs)
        }
    )
    #TODO:Set a limit of buying skills
    for elem in chosenBackground.learning:
        if isinstance(elem,MetaChoice):
            for subelem in elem.value:
                options.append(
                    {
                        "desc":f"Acquérir {subelem.value}",
                        "goto": (_selectSkill,{"skill":subelem,"chosenBackground":chosenBackground})
                    }
                )
        elif isinstance(elem,Skill):
            options.append(
                {
                    "desc":f"Acquérir {elem.value}",
                    "goto": (_selectSkill,{"skill":elem,"chosenBackground":chosenBackground})
                }
            )

    text = f"Sélection des compétences pour {chosenBackground.desc}"
    help = f"Un vrai casse-tête"
    #TODO:Maybe add option for growth table and random generatinon


    return (text, help), options

def _selectSkill(caller,rawString:str,skill:Skill,**kwargs):
    """Modify the needed skill"""
    tmpChar:tempCharSheet = caller.ndb._evmenu.tmpChar
    acquired = tmpChar.skills[skill][1]
    if acquired:
        tmpChar.skills[skill][0] += 1
        caller.msg(f"|wCompétence {str(skill)} = {tmpChar.skills[skill][0]}|n")
    else:
        tmpChar.skills[skill][1] = True
        caller.msg(f"|wCompétence {str(skill)} achetée|n")
    
    return "subNodeBackground",kwargs




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
    menutree = {
        "nodeChargen":nodeChargen,
        "nodeChangeName":nodeChangeName,
        "nodeRollStat":nodeRollStat,
        "nodeAssignStat":nodeAssignStat,
        "subnodeAssignStatHelper":subnodeAssignStatHelper,
        "nodeInfoBackgroundBase":nodeInfoBackgroundBase,
        "nodeSelectBackground":nodeSelectBackground,
        "subNodeBackground":subNodeBackground,
        "nodeApplyChargen":nodeApplyChargen,
    }

    tmpChar = tempCharSheet()

    def finishCharcb(session,menu):
        caller.msg("Création terminé")

    # Generate a template char
    EvMenu(caller,menutree,session=session,
           startnode="nodeChargen",tmpChar=tmpChar,cmd_on_exit=finishCharcb)