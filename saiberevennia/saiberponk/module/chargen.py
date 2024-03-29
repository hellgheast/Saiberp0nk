from world.rules import dice
from typeclasses.charinfohandler import CharInfoHandler
from module.enums import Stat, Skill, CharInfo, CombatMixin, Backgrounds, MetaChoice
from module.forms import EV_PC_SHEET_DICT
from typeclasses.characters import Character
from typing import List
from evennia import EvMenu
from textwrap import dedent


from evennia.utils.evform import EvForm
from evennia.utils.evtable import EvTable


_TEMP_SHEET = """
Prénom : {firstname} Nom: {lastname}
Origine: {background}
{sep1}
FOR:{FOR}\tINT:{INT}
SAG:{SAG}\tDEX:{DEX}
CON:{CON}\tCHA:{CHA}
{sep2}
{skillForm}

{desc}

"""


_SKILL_BUY_COUNTER = 2


class tempCharSheet:
    def __init__(self) -> None:
        # Base stats
        self.stats = {stat: 0 for stat in Stat.attributes()}
        # Skills
        self.skills = {skill: [-1, False] for skill in Skill.attributes()}
        # CharInfo
        self.charinfo = {ci: "" for ci in CharInfo.attributes()}
        # Combat Mixin
        self.combatmixin = {cm: "" for cm in CombatMixin.attributes()}
        # Defaults value for combatmixim atm
        self.combatmixin[CombatMixin.ATKBONUS] = 0
        self.combatmixin[CombatMixin.CW] = 0
        self.combatmixin[CombatMixin.RGARMORCLASS] = 10
        self.combatmixin[CombatMixin.CQDARMORCLASS] = 10

        # Description
        self.desc = "Zlatows, le super zlatis"

        # Stat array
        self.statArray: List[int] = [14, 12, 11, 10, 9, 7]

        # Maximum number of skill you can buy
        self.skillBuyCounter = _SKILL_BUY_COUNTER

        self.applyFreeSkill: bool = False
        self.lastStepDone: bool = False

    def showSheet(self):
        form = EvForm(data=EV_PC_SHEET_DICT)
        form.map(
            cells={
                1: self.charinfo[CharInfo.LASTNAME],
                2: self.charinfo[CharInfo.FIRSTNAME],
                3: self.charinfo[CharInfo.BACKGROUND],
                4: self.desc,
                5: self.stats[Stat.FOR],
                6: self.stats[Stat.INT],
                7: self.stats[Stat.SAG],
                8: self.stats[Stat.DEX],
                9: self.stats[Stat.CON],
                10: self.stats[Stat.CHA],
                11: self.combatmixin[CombatMixin.PV],
                12: self.combatmixin[CombatMixin.MAXPV],
            },
            tables={
                "A": EvTable(
                    "Compétence",
                    "Niveau",
                    "Acquis",
                    table=[
                        [x for x in self.skills.keys()],

                        [x[0] for x in self.skills.values()],
                        ["Oui " if x[1] else "Non" for x in self.skills.values()],
                    ],
                    border="incols",
                )
            },
        )

        return str(form)

    def buySkill(self, skill: Skill, free: bool = False) -> int:
        """
        Method to buy/improve skill and modify needed attributes
        Returns:
            value of the current skill
        """
        acquired = self.skills[skill][
            1
        ]  # Elem 1 is Bool, Elem 0 is the value of the skill
        if acquired:
            self.skills[skill][0] += 1
        else:
            self.skills[skill][0] = 0
            self.skills[skill][1] = True
        if free == False:
            self.skillBuyCounter -= 1
        return self.skills[skill][0]

    def resetStatAssignation(self):
        # Stat array
        self.statArray: List[int] = [14, 12, 11, 10, 9, 7]
        # Base stats
        self.stats = {stat: 0 for stat in Stat.attributes()}

    def resetSkillAssignation(self):
        # Skills dict
        self.skills = {skill: [-1, False] for skill in Skill.attributes()}
        self.skillBuyCounter = _SKILL_BUY_COUNTER
        self.applyFreeSkill = False

    def applyStats(self,char: Character):
        # Apply stats
        for stat, value in self.stats.items():
            char.traits[stat].base = int(value)

    def updateCombatMixin(self,char: Character):            
        self.applyStats(char)

        # Update computed properties and heal
        char.helper[CombatMixin.PV] = char.helper[CombatMixin.MAXPV]
        char.helper[CombatMixin.MAXCW]

        self.combatmixin[CombatMixin.PV] = char.helper[CombatMixin.PV]
        self.combatmixin[CombatMixin.MAXPV] = char.helper[CombatMixin.MAXPV]

        char.helper[CombatMixin.CW] = self.combatmixin[CombatMixin.CW]
        char.helper[CombatMixin.ATKBONUS] = self.combatmixin[CombatMixin.ATKBONUS]
        char.helper[CombatMixin.CQDARMORCLASS] = self.combatmixin[CombatMixin.CQDARMORCLASS]
        char.helper[CombatMixin.RGARMORCLASS] = self.combatmixin[CombatMixin.RGARMORCLASS]

    def apply(self, char: Character):
        try:
            # Apply stats
            self.applyStats(char)

            # Apply skills
            for skill, value in self.skills.items():
                char.traits[skill].acquired = value[1]
                char.traits[skill].base = value[0]
            # Apply charinfo
            for key, info in self.charinfo.items():
                char.charinfo[key] = info

            # Apply computed properties and other combatmixin
            self.updateCombatMixin(char)
            
            # Apply description (it is a db attribute)
            char.db.desc = self.desc
            
        except Exception as e:
            char.msg(f"{e}")


def nodeChargen(caller, rawString, **kwargs):
    """Main node"""
    # Workaround as kwargs are not correctly tranmitted
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar

    

    # options.append(
    #     {"desc": "Sélection d'origine", "goto": ("nodeInfoBackgroundBase", kwargs)}
    # )

    options = [{"desc": "À propos de Saiberponk", "goto": ("nodeAboutSaiberponk",kwargs)}]
    options.append(
         {"desc": "Commencer création de personnage", "goto": ("nodeBeginChargen", kwargs)}
    )
    if tmpChar.lastStepDone:

        options.append(
            {
                "desc": "Accepter et créer ton personnage",
                "goto": ("nodeApplyChargen", kwargs),
            },
        )
        tmpChar.updateCombatMixin(caller)

    text = tmpChar.showSheet()

    return text, options


def nodeAboutSaiberponk(caller, rawString, **kwargs):

    text = f"Saiberponk est un super jeu..."

    options = [{"desc": "retour au menu principal", "goto": ("nodeChargen", kwargs)}]

    return text, options


def nodeBeginChargen(caller, rawString, **kwargs):

    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar

    text = f"Il est temps de générer les statistiques de votre personnage\nLa génération aléatoire peut vous être bénéficiaire où pas !"

    tmpChar.resetStatAssignation()
    tmpChar.resetSkillAssignation()

    options = []
    options.append(
        {"desc": "Génération aléatoire de personnage", "goto": ("nodeRollStat", kwargs)}
    )
    options.append(
        {"desc": "Génération de personnage", "goto": ("nodeAssignStat", kwargs)}
    )

    return text, options


def _update_name(caller, rawString: str, **kwargs):
    """
    Used by node_change_name below to check what user
    entered and update the name if appropriate.

    """
    if rawString.strip():
        caller.msg(rawString)
        tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar
        if rawString.find(" ") != -1:
            tmpChar.charinfo[CharInfo.FIRSTNAME], tmpChar.charinfo[CharInfo.LASTNAME] = [
                x.lower().capitalize() for x in rawString.split(" ",maxsplit=1)
            ]
        else:
            tmpChar.charinfo[CharInfo.FIRSTNAME] = rawString

        caller.msg(f"Prénom: |w{tmpChar.charinfo[CharInfo.FIRSTNAME]}|n Nom: |w{tmpChar.charinfo[CharInfo.LASTNAME]}|n")
    return "nodeSetNameDesc", kwargs
    
def nodeChangeName(caller, rawString: str, **kwargs):
    """
    Change the random name of the character.

    """
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar

    text = (
        f"Ton nom actuel est |w{tmpChar.charinfo[CharInfo.FIRSTNAME]} {tmpChar.charinfo[CharInfo.LASTNAME]}|n. "
        "\nFormat: Prénom Nom"
        "\nLaisser vide pour interrompre la saisie."
    )

    options = {"key": "_default", "goto": (_update_name, kwargs)}

    return text, options



def _updateDesc(caller, rawString: str, **kwargs):
    """
    Used by node_change_name below to check what user
    entered and update the name if appropriate.

    """
    if rawString.strip():
        caller.msg(rawString)
        tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar
        tmpChar.desc = rawString
        caller.msg(f"Description: |w{tmpChar.desc}|n")
    return "nodeSetNameDesc", kwargs


def nodeSetDescription(caller,rawString: str, **kwargs):
    """
    Set the description of the character

    """
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar

    text = (
        f"""Ta description actuelle est :
        |w{tmpChar.desc}|n. "
        """
    )

    options = {"key": "_default", "goto": (_updateDesc, kwargs)}

    return text, options

def nodeRollStat(caller, rawString: str, **kwargs):
    caller.msg("Lancement des dés...")

    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar

    for stat in Stat.attributes():
        tmpChar.stats[stat] = dice.roll("3d6")
        caller.msg(f"{stat} = {tmpChar.stats[stat]}")

    text = f"Génération alétoire des statistiques du personnage"

    options = [{"desc": "sélection de l'origine du personnage", "goto": ("nodeInfoBackgroundBase", kwargs)}]

    return text, options


def _stat_assign_helper(caller, rawString: str, **kwargs):
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar
    selectedStat = kwargs.get("stat", None)

    if rawString:
        value = int(rawString)
        if value in tmpChar.statArray:
            tmpChar.stats[selectedStat.value] = value
            tmpChar.statArray.remove(value)
            caller.msg(f"{selectedStat} = {value}")
        else:
            caller.msg("Valeur |rinvalide|n")
    else:
        caller.msg("No assign")
    return "nodeAssignStat", kwargs


def subnodeAssignStatHelper(caller, rawString: str, **kwargs):
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar
    selectedStat = kwargs.get("stat", None)
    showStr = "\t".join([str(x) for x in tmpChar.statArray])

    text = (f"Insérer la valeur pour {selectedStat.value}\nDisponible:\n{showStr}",)

    options = {"key": "_default", "goto": (_stat_assign_helper, {"stat": selectedStat})}

    return text, options


def subnodeResetStat(caller, rawString: str, **kwargs):
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar
    tmpChar.resetStatAssignation()
    return "nodeAssignStat", kwargs


def nodeAssignStat(caller, rawString: str, **kwargs):
    """
    Node to assign the stats
    """

    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar

    def _isAssigned(stat: Stat) -> bool:
        nonlocal tmpChar
        if tmpChar.stats[stat] != 0:
            return True
        else:
            return False

    showStr = "\t".join([str(x) for x in tmpChar.statArray])

    if len(tmpChar.statArray) != 0:
        text = (f"Sélections des statistiques pour le personnage\n{showStr}",)
    else:
        text = f"Statistiques |gassignées|n"
    options = []

    # Generate submenu assignation
    for stat in Stat.enumList():
        if _isAssigned(stat) == False:
            options.append(
                {
                    "desc": f"Assigner |w{stat}|n",
                    "goto": ("subnodeAssignStatHelper", {"stat": stat}),
                },
            )

    options.append(
        {"desc": "Reset des statistiques", "goto": (subnodeResetStat, kwargs)}
    )

    if len(tmpChar.statArray) == 0:
        options.append(
            {"desc": "Sélection de l'orgine du personnage", "goto": ("nodeInfoBackgroundBase", kwargs)},
        )

    return text, options


#########################################################
#                 Informational Pages
#########################################################

# Thanks for Inspector Caracal for all the help
_BACKGROUND_INFO_DICT = {
    # The keys here are the different options you can choose, and the values are the info pages
    Backgrounds.BUM: dedent(
        """\
        Vagabond, junkie, vagabond... parfois "sans-abri" si quelqu'un essaie d'obtenir des dons. 
        La plupart de ceux qui se trouvent dans votre situation sont traités comme rien de plus 
        que des détritus humains à deux pas d'une tombe bienvenue. Vous êtes peut-être né dans 
        une pauvreté qui ne se distingue pas de l'indigence professionnelle ou peut-être 
        qu'un événement vous a fait tomber d'un niveau de vie élevé où d'une vie meilleure, 
        mais vous n'avez pas l'intention de vous laisser faire. Être un rebut de la société dans une 
        dystopie comme celle-ci est une chose à laquelle seuls les plus forts survivent longtemps.
        Avec les compétences que vous possédez, vous avez l'intention de faire bien plus que survivre.
        """
    ),
    Backgrounds.BUROCRAT: dedent(
        """\
        Il fallait bien que quelqu'un fasse tourner les roues du gouvernement, et vous étiez aussi bon que n'importe qui d'autre.
        Les gouvernements des villes ne sont peut-être guère plus que des coquilles pour l'exploitation des corpos, 
        mais à eux et leur armée de fonctionnaires maintiennent l'électricité, les bidonvilles et un semblant d'ordre civique. 
        Il peut s'agir d'un travail très lucratif pour ceux qui sont en mesure d'exiger des pots-de-vin et d'autres incitations, 
        mais il vous faudra percevoir votre prime de façon plus directe désormais.
        Vous savez comment fonctionne la machine, et cela peut valoir plus que n'importe quelle somme de balles.
        """
    ),
    Backgrounds.CLERGY: dedent(
        """\
        Dans les bidonvilles, les gens ne peuvent compter que sur leurs propres forces et sur la miséricorde de Dieu. 
        Au milieu du désespoir et la désolation de l'ère moderne, des milliers de croyances et de sectes différentes ont vu 
        le jour pour apporter du réconfort à leurs adeptes. La plupart d'entre elles sont des canaux de commercialisation parrainés 
        par des corpos pour vendre des retraites spirituelles, des artefacts bénis et des grades ecclésiastiques prestigieux, mais 
        quelques membres du clergé s'obstinent encore à servir Dieu avant Mammon. Ces renégats sont souvent livrés à eux-mêmes, 
        contraints de collecter leur propre dîme et de délivrer le juste jugement du Seigneur de leurs propres mains.
        """
    ),
    Backgrounds.CODER: dedent(
        """\
        Le monde de l'entreprise repose sur du code, et vous êtes l'une des personnes qui le font tourner.
        Les codeurs sont trop étroitement surveillés pour travailler en tant qu'opérateurs.
        mais l'écosystème des freelances, des prodiges autodidactes et des grimpeurs désespérés est toujours
        riche en opportunités. Vous pouvez être un véritable hacker, capable d'exécuter du code dans les situations les plus
        stressantes, ou vous pouvez orienter vos compétences d'opérateur dans une direction plus physique, en gardant 
        vos connaissances en programmation comme un outil de secours pour les cas où votre arme préférée ne convient pas.
        """
    ),
    Backgrounds.CORPSEC: dedent(
        """\
        Il y a des gens que l'on déteste plus que la sécurité corporatiste,
        mais la plupart d'entre eux sont impliqués dans des querelles de sang, des guerres de religion ou des vendettas éternelles.
        Vous avez certainement laissé l'uniforme derrière vous, mais vous mais vous vous souvenez encore du fonctionnement du monde corporatiste,
        et, plus important encore, du fonctionnement de ses unités de sécurité. 
        Vous avez peut-être encore un contact dans la corporation que vous avez quittée, ou une raison particulière de leur en vouloir.
        En tant qu'ancien agent de sécurité, tout le monde sait que vous ne reviendrez jamais. Les corporations ne vous laisseront jamais vivre.
        """
    )
}


def nodeInfoBackgroundBase(caller, rawString: str, **kwargs):
    """Information générale avant la sélection d'un background particulier"""
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar
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
        {"desc": "retour au menu principal", "goto": ("nodeChargen", kwargs)},
    ]

    # Safeguard: reset the skills whenever they have been applied
    if tmpChar.applyFreeSkill:
        tmpChar.resetSkillAssignation()

    # Generate submenu assignation
    for bg in _BACKGROUND_INFO_DICT.keys():
        options.append(
            {
                "desc": f"En savoir plus sur |w{bg.desc}|n",
                "goto": ("nodeSelectBackground", {"chosenBackground": bg}),
            },
        )

    return (text, help), options


def _showBackgroundSkill(bg: Backgrounds) -> str:
    """Fonction pour afficher correctement les compétences disponibles"""
    bgSheet: str = dedent(
        f"""
    Origine: |c{bg.desc}|n Compétence gratuite: |015{bg.freeSkill if isinstance(bg.freeSkill,Skill) else MetaChoice.MetaChoice2str(bg.freeSkill) }|n
    """
    )

    learningSheet: str = "Compétences disponibles\n"
    for elem in bg.learning:
        if isinstance(elem, MetaChoice):
            learningSheet += "{}\n".format(MetaChoice.MetaChoice2str(elem))
        elif isinstance(elem, Skill):
            learningSheet += "{}/{}\n".format(elem.value, Skill.shortNames(elem))
        else:
            # Show error
            learningSheet += "ERROR"
    completeStr = dedent(
        f"""\
    {bgSheet}
    {15*"-"}
    {learningSheet}
    """
    )
    return completeStr


def nodeSelectBackground(
    caller, rawString: str, chosenBackground: Backgrounds = None, **kwargs
):
    """Noeud d'information qui affiche les informations à propos de cette origine"""
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar

    if not chosenBackground:
        return "no chosenBackground !"

    text = dedent(f"|w{_BACKGROUND_INFO_DICT[chosenBackground]}|n {_showBackgroundSkill(chosenBackground)} ")
    help = f"Information concernant l'origine {chosenBackground.desc}"

    options = [
        {"desc": "retour au menu principal", "goto": ("nodeChargen", kwargs)},
    ]
    options.append(
        {
            "desc": f"Devenir |g{chosenBackground.desc}|n",
            "goto": ("subNodeBackground", {"chosenBackground": chosenBackground}),
        }
    )

    # Generate submenu assignation
    for bg in _BACKGROUND_INFO_DICT.keys():
        if bg != chosenBackground:
            options.append(
                {
                    "desc": f"En savoir plus sur |w{bg.desc}|n",
                    "goto": ("nodeSelectBackground", {"chosenBackground": bg}),
                },
            )

    return (text, help), options


def subNodeBackground(
    caller, rawString: str, chosenBackground: Backgrounds = None, **kwargs
):
    """Noeud de sélection qui permet la sélection des compétences de cette origine"""
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar

    if not chosenBackground:
        return "no chosenBackground !"

    options = []

    if tmpChar.skillBuyCounter == 0:
        options.append(
            {
                "desc": "Valider origine et compétences",
                "goto": (_validateBackground, {"chosenBackground": chosenBackground}),
            }
        )

    options.append(
        {
            "desc": "Reset des compétences assignées",
            "goto": (subnodeResetSkill, {"chosenBackground": chosenBackground}),
        }
    )

    selectedSkills = kwargs.get("selectedSkills", [])

    # First time we enter here we apply or select the free skill
    if tmpChar.applyFreeSkill == False:
        if isinstance(chosenBackground.freeSkill, MetaChoice):
            for elem in chosenBackground.freeSkill.value:
                options.append(
                    {
                        "desc": f"Acquérir |ggratuitement|n {elem.value}",
                        "goto": (
                            _selectSkill,
                            {
                                "skill": elem,
                                "chosenBackground": chosenBackground,
                                "free": True,
                            },
                        ),
                    }
                )

        elif isinstance(chosenBackground.freeSkill, Skill):
            tmpChar.buySkill(chosenBackground.freeSkill, True)
            caller.msg(f"Compétence {chosenBackground.freeSkill} gratuite appliquée")
            selectedSkills.append(
                chosenBackground.freeSkill
            )  # So we know we already acquired it
            tmpChar.applyFreeSkill = True

    # TODO:Set a limit of buying skills
    if tmpChar.skillBuyCounter > 0:
        for elem in chosenBackground.learning:
            if isinstance(elem, MetaChoice):
                for subelem in elem.value:
                    if subelem in selectedSkills:
                        optStr = f"|g{subelem.value}|n"
                    else:
                        optStr = f"{subelem.value}"
                    options.append(
                        {
                            "desc": f"Acquérir {optStr}",
                            "goto": (
                                _selectSkill,
                                {
                                    "skill": subelem,
                                    "selectedSkills": selectedSkills,
                                    "chosenBackground": chosenBackground,
                                },
                            ),
                        }
                    )
            elif isinstance(elem, Skill):
                if elem in selectedSkills:
                    optStr = f"|g{elem.value}|n"
                else:
                    optStr = f"{elem.value}"
                options.append(
                    {
                        "desc": f"Acquérir {optStr}",
                        "goto": (
                            _selectSkill,
                            {
                                "skill": elem,
                                "selectedSkills": selectedSkills,
                                "chosenBackground": chosenBackground,
                            },
                        ),
                    }
                )

    options.append(
        {
            "desc": "retour au menu de sélection des origines",
            "goto": ("nodeInfoBackgroundBase", kwargs),
        }
    )



    text = f"Sélection des compétences pour {chosenBackground.desc}\nPoints de compétences restants: {tmpChar.skillBuyCounter}"
    help = f"Un vrai casse-tête"
    # TODO:Maybe add option for growth table and random generatinon

    return (text, help), options


def _selectSkill(
    caller,
    rawString: str,
    skill: Skill,
    free: bool = False,
    selectedSkills: List[Skill] = [],
    **kwargs,
):
    """Modify the needed skill and render the correct message"""
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar
    skillValue = tmpChar.buySkill(skill, free)
    if free == True:
        tmpChar.applyFreeSkill = True
    if skillValue > 0:
        caller.msg(f"|wCompétence {str(skill)} = {tmpChar.skills[skill][0]}|n")
    else:
        caller.msg(f"|wCompétence {str(skill)} achetée|n")
    selectedSkills.append(skill)
    return (
        "subNodeBackground",
        {
            "selectedSkills": selectedSkills,
            "chosenBackground": kwargs.get("chosenBackground"),
        },
    )


def _validateBackground(
    caller, rawString: str, chosenBackground: Backgrounds = None, **kwargs
):
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar
    if not chosenBackground:
        return "no chosenBackground :validateBackground"

    tmpChar.charinfo[CharInfo.BACKGROUND] = chosenBackground.desc
    caller.msg(f"Origine {chosenBackground.desc} sélectionné !")
    

    return "nodeSetNameDesc", kwargs


def subnodeResetSkill(caller, rawString: str, **kwargs):
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar
    tmpChar.resetSkillAssignation()
    caller.msg("Reset des compétences effectué !")
    return "subNodeBackground", kwargs


def nodeSetNameDesc(caller, rawString: str, **kwargs):
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar

    text = f"Il est temps de donner un nom et une description à ton personnage."
    options = [{"desc": "Choisir ton nom", "goto": ("nodeChangeName", kwargs)}]
    options.append(
        {"desc": "Faire sa description", "goto": ("nodeSetDescription", kwargs)}
    )
    options.append(
        {"desc": "|gValider nom et description|n", "goto": ("nodeChargen", kwargs)}
    )

    tmpChar.lastStepDone = True

    return text,options

def nodeApplyChargen(caller, rawString: str, **kwargs):
    """
    End chargen and create the character. We will also puppet it.

    """
    tmpChar: tempCharSheet = caller.ndb._evmenu.tmpChar
    tmpChar.apply(caller)

    text = "Personnage crée !"

    return text, None


def startChargen(caller, session=None):
    """
    Starting point
    """
    menutree = {
        "nodeChargen": nodeChargen,
        "nodeBeginChargen":nodeBeginChargen,
        "nodeAboutSaiberponk":nodeAboutSaiberponk,
        "nodeRollStat": nodeRollStat,
        "nodeAssignStat": nodeAssignStat,
        "subnodeAssignStatHelper": subnodeAssignStatHelper,
        "nodeInfoBackgroundBase": nodeInfoBackgroundBase,
        "nodeSelectBackground": nodeSelectBackground,
        "subNodeBackground": subNodeBackground,
        "nodeSetNameDesc":nodeSetNameDesc,
        "nodeSetDescription":nodeSetDescription,
        "nodeChangeName": nodeChangeName,
        "nodeApplyChargen": nodeApplyChargen,
    }

    tmpChar = tempCharSheet()

    def finishCharcb(session, menu):
        caller.msg("Création terminé")

    # Generate a template char
    EvMenu(
        caller,
        menutree,
        session=session,
        startnode="nodeChargen",
        tmpChar=tmpChar,
        cmd_on_exit=finishCharcb,
    )
