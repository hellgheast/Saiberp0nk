from commands.command import Command
from commands.command import MuxCommand
from evennia import CmdSet
import evennia
from evennia import set_trace, default_cmds
from world import rules
from module import cinematic
from module.enums import Stat, CharInfo, CombatMixin, Skill, WieldLocation
from evennia.utils.evform import EvForm
from evennia.utils.evtable import EvTable
from module.forms import EV_PC_SHEET_DICT
from textwrap import dedent

# Main commands for testing and debugging


class CmdEchelon(Command):
    """
    Commande de base pour appeller Echelon
    """

    key = "echelon"

    def func(self):
        if self.args:
            self.caller.msg(f"Ordres\t: [{self.args}]")
            if "traitre" in self.args:
                cinematic.sendArrayText(
                    self.caller,
                    [
                        ("|rEspèce de salopard !|n", 1),
                        ("|304Je vais envoyer les TacMercs à tes trousses !|n", 1),
                        ("|550Fais tes prières !!|n", 1),
                        (
                            "|n|rERREUR: |yUTILISATEUR NON EXISTANT|n //..//.. |rDÉCONNEXION!!|n\n",
                            2,
                        ),
                    ],
                )
        else:
            textList = [
                (f"|gBonjour {self.caller.key} je suis Echelon charcudoc 2 !|n\n", 2),
                ("|g.", 1),
                ("|g.", 1),
                ("|g.", 1),
                ("|gDemande d'accès|n ... |rCODE ROUGE|n", 0),
                (".", 1),
                (".", 1),
                (".", 1),
                ("|bAccès accordé|n\n", 5),
            ]
            cinematic.sendArrayText(self.caller, textList)


class CmdOpenModal(Command):
    """
    Fonction qui teste les fonctionnalités du client web
    """

    key = "openmodal"

    def parse(self):
        pass

    def func(self):
        caller = self.caller
        caller.msg(("|bTestMenu", {"type": "popup"}))
        caller.msg(("|rTestMap", {"type": "map"}))


class CmdMobAdd(Command):
    """
    Fonction pour rajouter un mob pour faire des essais
    """

    key = "mobadd"

    def parse(self):
        pass

    def func(self):
        evennia.create_object(
            "typeclasses.monsters.ArachBot",
            key="ArachTest",
            location=self.caller.location,
        )


class CmdPrendre(default_cmds.CmdGet):
    """
    Commande pour prendre des objets
    """

    key = "prendre"
    aliases = "obtenir"
    locks = "cmd:all();view:perm(Developer);read:perm(Developer)"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        if not self.args:
            caller.msg("Prendre quoi ?")
            return
        obj = caller.search(self.args, location=caller.location)
        if not obj:
            return
        if caller == obj:
            caller.msg("Tu ne peux pas te prendre toi-même.")
            return
        if not obj.access(caller, "get"):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("Tu ne peux pas prendre celà.")
            return

        # calling at_pre_get hook method
        if not obj.at_pre_get(caller):
            return

        success = obj.move_to(caller, quiet=True, move_type="get")
        if not success:
            caller.msg("Ceci ne peux pas être pris.")
        else:
            singular, _ = obj.get_numbered_name(1, caller)
            # TODO: Add inline func $Tu()
            caller.location.msg_contents(f"$You() prends {singular}.", from_obj=caller)
            # calling at_get hook method
            obj.at_get(caller)


class CmdFindTerm(Command):
    """
    Commande pour trouver un terminal
    """

    key = "recherche_terminal"

    def func(self):
        comterm = self.caller.search("comterm")
        if not comterm:
            return
        else:
            self.caller.msg("Un comterm est disponible !")


class CmdInfo(Command):
    """
    Commande d'information sur ton personnage
    """

    key = "info"

    def func(self):
        caller = self.caller
        if not self.args:
            target = self.caller
        else:
            # FIXME: Broken research
            target = self.caller.search(self.args)
            if not target:
                return
        # try to get stats
        # from evennia import set_trace;set_trace()

        form = EvForm(data=EV_PC_SHEET_DICT)
        genSkill = {
            k: [target.traits[k].value, target.traits[k].acquired]
            for k in Skill.attributes()
        }
        form.map(
            cells={
                1: target.charinfo[CharInfo.LASTNAME],
                2: target.charinfo[CharInfo.FIRSTNAME],
                3: target.charinfo[CharInfo.BACKGROUND],
                4: target.return_appearance(caller),
                5: target.traits[Stat.FOR].value,
                6: target.traits[Stat.INT].value,
                7: target.traits[Stat.SAG].value,
                8: target.traits[Stat.DEX].value,
                9: target.traits[Stat.CON].value,
                10: target.traits[Stat.CHA].value,
                11: target.helper[CombatMixin.PV],
                12: target.helper[CombatMixin.MAXPV],
            },
            tables={
                "A": EvTable(
                    "Compétence",
                    "Niveau",
                    "Acquis",
                    table=[
                        [x for x in genSkill.keys()],
                        [x[0] for x in genSkill.values()],
                        ["Oui " if x[1] else "Non" for x in genSkill.values()],
                    ],
                    border="incols",
                )
            },
        )
        self.caller.msg(text=str(form))


class CmdStatCheck(Command):
    """
    Debug command for StatCheck

    Usage:
        statcheck statName targetNumber

    """

    key = "statcheck"

    def parse(self):
        if not self.args:
            self.statName = None
            self.targetNumber = None
        else:
            statName, targetNumber = self.args.strip().split(" ")
            self.statName = statName
            self.targetNumber = int(targetNumber)

    def func(self):
        caller = self.caller

        if self.statName == None and self.targetNumber == None:
            caller.msg("Missing arguments")
            return

        result = rules.rollStatCheck(caller, self.statName, self.targetNumber, True)
        if result:
            caller.msg(f"{self.statName} ROLL SUCCESS")
        else:
            caller.msg(f"{self.statName} ROLL FAILURE")


class CmdInventory(Command):
    """
    Commande pour voir son inventaire

    Usage:
        inventaire

    """

    key = "inventaire"
    aliases = ("i", "inv")

    def func(self):
        caller = self.caller

        loadout = caller.inventory.displayLoadout()
        backpack = caller.inventory.displayBackpack()
        carryUsage = caller.inventory.displayCarryUsage()
        caller.msg(f"{loadout}\n{backpack}\n{carryUsage}")


class CmdWieldOrWear(Command):
    """
    Équiper une arme/un équipement or porter une armure/un casque

    Usage:
        équiper <objet>
        porter <objet>

    """

    key = "équiper"
    aliases = ("porter",)

    out_txts = {
        WieldLocation.BACKPACK: "Tu mets {key} dans ton sac à dos.",
        WieldLocation.LEGS: "Tu enfiles {key} sur tes jambes.",
        WieldLocation.TWO_HANDS: "Tu prends {key} à deux mains.",
        WieldLocation.LEFT_HAND: "Tu prends {key} avec ta main gauche.",
        WieldLocation.RIGHT_HAND: "Tu prends {key} avec ta main droite.",
        WieldLocation.BODY: "Tu enfiles {key} sur toi même.",
        WieldLocation.HEAD: "Tu mets {key} sur ta tête.",
    }

    def func(self):
        # find the item among those in equipment
        item = self.caller.search(
            self.args, candidates=self.caller.inventory.all(onlyObj=True)
        )
        self.caller.msg(f"item {item}")
        if not item:
            # An 'item not found' error will already have been reported; we add another line
            # here for clarity.
            self.caller.msg("Tu dois avoir les objets que tu souhaites équiper/porter.")
            return

        useSlot = getattr(item, "useSlot", WieldLocation.BACKPACK)

        # check what is currently in this slot
        current = self.caller.inventory.slots[useSlot]

        if current == item:
            self.caller.msg(f"Tu utilises déjà {item.key}.")
            return

        # move it to the right slot based on the type of object
        self.caller.inventory.move(item)

        # inform the user of the change (and potential swap)
        if current:
            self.caller.msg(f"Tu remets {current.key} dans ton sac à dos.")
        self.caller.msg(self.out_txts[useSlot].format(key=item.key))


class CmdExport(MuxCommand):

    """

    Tool to export things to a string that can be imported elsewhere with the import command.


    Usage:

        export          - Export the current room, and all it's attributes, locks, and tags.

        export/all      - Export the current room, and all objects within it.

        export <object> - Export a single object.



    """

    key = "export"

    help_category = "Building"

    locks = "perm(Builder)"

    def func(self):
        caller = self.caller

        export_dict = {}

        if self.args:
            target = self.caller.search(self.args)

            if not target:
                self.caller.msg("|x[|rERROR|x]|M Object was not found.")

                return

            if target.is_typeclass(
                "typeclasses.characters.Character", exact=False
            ) or target.is_typeclass("typeclasses.exits.Exit", exact=False):
                self.caller.msg(
                    "|x[|rERROR|x]|M You cannot export Characters or Exits."
                )

                return

            export_dict["objects"] = []

            key = target.key

            typeclass = target.typeclass_path

            locks = target.locks.get()

            aliases = target.aliases.all()

            # TODO:check how to remove the dbref in the aliases
            aliases = [x for x in aliases if str(target.id) not in x]

            tags = target.tags.all(return_key_and_category=True)

            obj_attr = []

            for attribute in target.attributes.all():
                obj_attr.append((attribute.key, attribute.value))

            export_dict["objects"].append(
                {
                    "key": key,
                    "typeclass": typeclass,
                    "aliases": aliases,
                    "locks": locks,
                    "tags": tags,
                    "attributes": obj_attr,
                }
            )

            self.caller.msg(
                f"Here's your Export String for {target.name}:\n{export_dict}"
            )
            # self.caller.popup(export_dict,f"|x>>|wExporting {target.name}",True)

            return

        # Handle location itself.

        export_dict["room"] = {}

        export_dict["room"]["key"] = self.caller.location.key

        export_dict["room"]["typeclass"] = self.caller.location.typeclass_path

        export_dict["room"]["locks"] = self.caller.location.locks.get()

        export_dict["room"]["tags"] = self.caller.location.tags.all(
            return_key_and_category=True
        )

        loc_attr = []

        for attribute in self.caller.location.attributes.all():
            loc_attr.append((attribute.key, attribute.value))

        export_dict["room"]["attributes"] = loc_attr

        if "all" in self.switches:
            export_dict["objects"] = []

            for obj in caller.location.contents:
                if obj.is_typeclass(
                    "typeclasses.characters.Character", exact=False
                ) or obj.is_typeclass("typeclasses.exits.Exit", exact=False):
                    continue

                obj_dict = {}

                obj_dict["key"] = obj.key

                obj_dict["typeclass"] = obj.typeclass_path

                obj_dict["locks"] = obj.locks.get()

                obj_dict["aliases"] = obj.aliases.get()

                obj_dict["tags"] = obj.tags.all(return_key_and_category=True)

                obj_attr = []

                for attribute in obj.attributes.all():
                    obj_attr.append((attribute.key, attribute.value))

                obj_dict["attributes"] = obj_attr

                export_dict["objects"].append(obj_dict)

        # self.caller.popup(export_dict,f"|x>>|wExporting |g{self.caller.location.name}",True)
        self.caller.msg(f"Here's your Export String: {export_dict}")


class CmdImport(MuxCommand):

    """

    Tool to import things from a string that was exported elsewhere with the export command.


    Usage:

        import                  - Open up the Import Editor window.

        import/string <string>  - Bypass edit and directly import using a given import string.




    """

    key = "import"

    help_category = "Building"

    switches = ["string"]

    locks = "perm(Builder)"

    def func(self):
        caller = self.caller

        def okf(boold):
            if boold:
                return "|x[|GOK|x]"

            if not boold:
                return "|x[|RFAIL|x]"

        if "string" in self.switches:
            if not self.args:
                self.caller.msg(
                    "|x[|rERROR|x]|M A string needs to be provided to import."
                )

                return

            try:
                import ast

                import_data = ast.literal_eval(self.args)

                if not isinstance(import_data, dict):
                    self.caller.msg(
                        "|x[|rERROR|x]|M The import string was invalid or corrupted. Please make sure your exported string is valid JSON."
                    )

                    return

                # Here we go!

                for obj in import_data:
                    if obj == "room":
                        caller.msg("|xImporting Room...")

                        key, locks, tags, attributes = (
                            import_data[obj].get("key", False),
                            import_data[obj].get("locks", False),
                            import_data[obj].get("tags", False),
                            import_data[obj].get("attributes", False),
                        )

                        if not key or not locks or not attributes:
                            self.caller.msg(
                                "|x[|rERROR|x]|M Import Data must contain at least the following data: key, locks, attributes."
                            )

                            return

                        tar = self.caller.location

                        tar.key = key

                        caller.msg(f"|xChanging Key to |g{key}|x... {okf(True)}")

                        lock = tar.locks.replace(locks)

                        caller.msg(f"|xUpdating locks... {okf(lock)}")

                        try:
                            tar.attributes.clear()

                            for key, value in attributes:
                                tar.attributes.add(key, value)

                            tar.tags.clear()

                            if tags:
                                for tag, category in tags:
                                    tar.tags.add(tag, category=category)

                            result = True

                        except:
                            result = False

                        caller.msg(
                            f"|w{len(attributes)}|x Attributes and |w{len(tags)}|x Tags Processed... {okf(result)}"
                        )

                    if obj == "objects":
                        objects = import_data[obj]

                        result = True

                        for item in objects:
                            try:
                                key, locks, tags, attributes = (
                                    item.get("key", False),
                                    item.get("locks", False),
                                    item.get("tags", False),
                                    item.get("attributes", False),
                                )

                                typeclass, aliases = item.get(
                                    "typeclass", False
                                ), item.get("aliases", [])

                                if (
                                    not key
                                    or not locks
                                    or not attributes
                                    or not typeclass
                                ):
                                    self.caller.msg(
                                        "|x[|rERROR|x]|M Import Data must contain at least the following data: key, typeclass, locks, attributes."
                                    )

                                    return

                                target = self.caller.location.search(
                                    key
                                )  # ,exact=True,quiet=True)[0]

                                if target:
                                    self.caller.msg(f"|xUpdating {target.name}|x...")

                                    target.aliases.clear()

                                    for alias in aliases:
                                        target.aliases.add(alias)

                                    target.aliases.add(target.id)

                                    target.locks.replace(locks)

                                else:
                                    self.caller.msg(
                                        f"|xCreating |=v{key} |x(|w{typeclass}|x)..."
                                    )

                                    from evennia.utils import create

                                    target = create.create_object(
                                        typeclass,
                                        key,
                                        self.caller,
                                        home=self.caller,
                                        aliases=aliases,
                                        locks=locks,
                                    )

                                    target.home = self.caller.location

                                    target.move_to(self.caller.location, quiet=True)

                                for key, value in attributes:
                                    target.attributes.add(key, value)

                                if tags:
                                    for tag, category in tags:
                                        target.tags.add(tag, category=category)

                            except:
                                result = False

                        caller.msg(
                            f"|w{len(objects)}|x Objects Processed... {okf(result)}"
                        )

            except:
                self.caller.msg(
                    "|x[|rERROR|x]|M The import string was invalid or corrupted. Please make sure your exported string is valid JSON."
                )

            return


class CustomCmdSet(CmdSet):
    """Set de commandes spéciales"""

    def at_cmdset_creation(self):
        self.add(CmdEchelon)
        self.add(CmdMobAdd)
        self.add(CmdFindTerm)
        self.add(CmdInfo)
        self.add(CmdStatCheck)
        self.add(CmdInventory)
        self.add(CmdWieldOrWear)
        self.add(CmdOpenModal)
        self.add(CmdImport)
        self.add(CmdExport)
