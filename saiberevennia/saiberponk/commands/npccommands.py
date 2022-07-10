from commands.command import Command
from evennia import CmdSet
from evennia import set_trace,default_cmds
from evennia import create_object

# refactor both commands to take in account traits model
class CmdCreateNPC(Command):
    """
    create a new npc

    Usage:
        createNPC <name>

    Creates a new, named NPC. The NPC will start with a all stats at 1.
    """
    key = "createnpc"
    aliases = ["createNPC","creerpnj"]
    locks = "call:not perm(nonpcs)"
    help_category = "builder"
    
    def func(self):
        """creates the object and names it"""
        caller = self.caller
        if not self.args:
            caller.msg("Usage: createNPC <name>")
            return
        if not caller.location:
            # may not create npc when OOC
            caller.msg("You must have a location to create an npc.")
            return
        # make name always start with capital letter
        name = self.args.strip().capitalize()
        # create npc in caller's location
        npc = create_object("characters.Character",
                      key=name,
                      location=caller.location,
                      locks="edit:id(%i) and perm(Builders);call:false()" % caller.id)
        
        npc.db.strength = 1
        npc.db.dexterity = 1
        npc.db.intelligence = 1
        npc.db.desc = "A dumb npc"
        # announce
        #TODO: f-string
        message = "%s created the NPC '%s'."
        caller.msg(message % ("You", name))
        caller.location.msg_contents(message % (caller.key, name),
                                                exclude=caller)

class CmdEditNPC(Command):
    """
    Edit an existing npc

    Usage:
        editnpc <name>[/<attribute> [= value]]

    Examples:
      editnpc mynpc/strength = 5
      editnpc mynpc/strength - displays strength value
      editnpc mynpc          - shows all editable
                                attributes and values

    This command edits an existing NPC. You must have
    permission to edit the NPC to use this.
"""

    key = "editnpc"
    aliases = ["editNPC","editerpnj"]
    locks = "call:not perm(nonpcs)"
    help_category = "builder"

    def parse(self):
        args = self.args
        propname, propval = None, None
        if "=" in args:
            args, propval = [part.strip() for part in args.rsplit("=", 1)]
        if "/" in args:
            args, propname = [part.strip() for part in args.rsplit("/", 1)]
        # store, so we can access it below in func()
        self.name = args
        self.propname = propname
        # a propval without a propname is meaningless
        self.propval = propval if propname else None
    
    def func(self):
        allowed_propnames = {"strength":int,
                            "dexterity":int,
                            "intelligence":int,
                            "firstname":str,
                            "lastname":str,
                            "age":int,
                            "height":int,
                            "weight":float,
                            "xp":int}
                            
                            

        caller = self.caller
        if not self.args or not self.name:
            caller.msg("Usage: +editnpc name[/propname][=propval]")
            return
        npc = caller.search(self.name)
        if not npc:
            return
        if not npc.access(caller, "edit"):
            caller.msg("You cannot change this NPC.")
            return
        if not self.propname:
            # this means we just list the values
            output = f"Properties of {npc.key}:"
            for propname,proptype in allowed_propnames.items():
                output += f"\n {propname} = {npc.attributes.get(propname, default='N/A')}"
            caller.msg(output)
        elif self.propname not in allowed_propnames:
            caller.msg(f"You may only change {', '.join(allowed_propnames.keys())}.")
        elif self.propval:
            # assigning a new propvalue
            # in this example, the properties are all integers...
            proptype = allowed_propnames[self.propname]
            typedpropval = proptype(self.propval)
            npc.attributes.add(self.propname, typedpropval)
            caller.msg(f"Set {npc.key}'s property {self.propname} to {self.propval}")
        else:
            # propname set, but not propval - show current value
            caller.msg(f"{npc.key} has property {self.propname} = {npc.attributes.get(self.propname,default='N/A')}")


class CmdNPC(Command):
    """
    controls an NPC

    Usage:
        npc <name> = <command>

    This causes the npc to perform a command as itself. It will do so
    with its own permissions and accesses.
    """
    key = "npc"
    locks = "call:not perm(nonpcs)"
    help_category = "builder"

    def parse(self):
        "Simple split of the = sign"
        name, cmdname = None, None
        if "=" in self.args:
            name, cmdname = self.args.rsplit("=", 1)
            name = name.strip()
            cmdname = cmdname.strip()
        self.name, self.cmdname = name, cmdname

    def func(self):
        "Run the command"
        caller = self.caller
        if not self.cmdname:
            caller.msg("Usage: npc <name> = <command>")
            return
        npc = caller.search(self.name)
        if not npc:
            return
        if not npc.access(caller, "edit"):
            caller.msg("You may not order this NPC to do anything.")
            return
        # send the command order
        npc.execute_cmd(self.cmdname)
        caller.msg(f"You told {npc.key} to do '{self.cmdname}'.")

class NpcCmdSet(CmdSet):
    """Set de commandes pour les npcs"""

    key = "builder"
    def at_cmdset_creation(self):
        self.add(CmdCreateNPC)
        self.add(CmdEditNPC)
        self.add(CmdNPC)