"""
Object

The Object is the "naked" base class for things in the game world.

Note that the default Character, Room and Exit does not inherit from
this Object, but from their respective default implementations in the
evennia library. If you want to use this class as a parent to change
the other types, you can do so by adding this as a multiple
inheritance.

"""
from evennia.objects.objects import DefaultObject
from evennia import AttributeProperty, create_object, search_object
from evennia.utils.utils import make_iter
from module.utils import get_obj_stats
from module.enums import WieldLocation,ObjType,WeaponType,Stat,Skill,CombatMixin
from world.rules import dice


class ObjectParent:
    """
    This is a mixin that can be used to override *all* entities inheriting at
    some distance from DefaultObject (Objects, Exits, Characters and Rooms).

    Just add any method that exists on `DefaultObject` to this class. If one
    of the derived classes has itself defined that same hook already, that will
    take precedence.

    """


class Object(ObjectParent, DefaultObject):
    """
    This is the root typeclass object, implementing an in-game Evennia
    game object, such as having a location, being able to be
    manipulated or looked at, etc. If you create a new typeclass, it
    must always inherit from this object (or any of the other objects
    in this file, since they all actually inherit from BaseObject, as
    seen in src.object.objects).

    The BaseObject class implements several hooks tying into the game
    engine. By re-implementing these hooks you can control the
    system. You should never need to re-implement special Python
    methods, such as __init__ and especially never __getattribute__ and
    __setattr__ since these are used heavily by the typeclass system
    of Evennia and messing with them might well break things for you.


    * Base properties defined/available on all Objects

     key (string) - name of object
     name (string)- same as key
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation

     account (Account) - controlling account (if any, only set together with
                       sessid below)
     sessid (int, read-only) - session id (if any, only set together with
                       account above). Use `sessions` handler to get the
                       Sessions directly.
     location (Object) - current location. Is None if this is a room
     home (Object) - safety start-location
     has_account (bool, read-only)- will only return *connected* accounts
     contents (list of Objects, read-only) - returns all objects inside this
                       object (including exits)
     exits (list of Objects, read-only) - returns all exits from this
                       object, if any
     destination (Object) - only set if this object is an exit.
     is_superuser (bool, read-only) - True/False if this user is a superuser

    * Handlers available

     aliases - alias-handler: use aliases.add/remove/get() to use.
     permissions - permission-handler: use permissions.add/remove() to
                   add/remove new perms.
     locks - lock-handler: use locks.add() to add new lock strings
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().
     sessions - sessions-handler. Get Sessions connected to this
                object with sessions.get()
     attributes - attribute-handler. Use attributes.add/remove/get.
     db - attribute-handler: Shortcut for attribute-handler. Store/retrieve
            database attributes using self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create
            a database entry when storing data

    * Helper methods (see src.objects.objects.py for full headers)

     search(ostring, global_search=False, attribute_name=None,
             use_nicks=False, location=None, ignore_errors=False, account=False)
     execute_cmd(raw_string)
     msg(text=None, **kwargs)
     msg_contents(message, exclude=None, from_obj=None, **kwargs)
     move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
     copy(new_key=None)
     delete()
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hooks (these are class methods, so args should start with self):

     basetype_setup()     - only called once, used for behind-the-scenes
                            setup. Normally not modified.
     basetype_posthook_setup() - customization in basetype, after the object
                            has been created; Normally not modified.

     at_object_creation() - only called once, when object is first created.
                            Object customizations go here.
     at_object_delete() - called just before deleting an object. If returning
                            False, deletion is aborted. Note that all objects
                            inside a deleted object are automatically moved
                            to their <home>, they don't need to be removed here.

     at_init()            - called whenever typeclass is cached from memory,
                            at least once every server restart/reload
     at_cmdset_get(**kwargs) - this is called just before the command handler
                            requests a cmdset from this object. The kwargs are
                            not normally used unless the cmdset is created
                            dynamically (see e.g. Exits).
     at_pre_puppet(account)- (account-controlled objects only) called just
                            before puppeting
     at_post_puppet()     - (account-controlled objects only) called just
                            after completing connection account<->object
     at_pre_unpuppet()    - (account-controlled objects only) called just
                            before un-puppeting
     at_post_unpuppet(account) - (account-controlled objects only) called just
                            after disconnecting account<->object link
     at_server_reload()   - called before server is reloaded
     at_server_shutdown() - called just before server is fully shut down

     at_access(result, accessing_obj, access_type) - called with the result
                            of a lock access check on this object. Return value
                            does not affect check result.

     at_pre_move(destination)             - called just before moving object
                        to the destination. If returns False, move is cancelled.
     announce_move_from(destination)         - called in old location, just
                        before move, if obj.move_to() has quiet=False
     announce_move_to(source_location)       - called in new location, just
                        after move, if obj.move_to() has quiet=False
     at_post_move(source_location)          - always called after a move has
                        been successfully performed.
     at_object_leave(obj, target_location)   - called when an object leaves
                        this object in any fashion
     at_object_receive(obj, source_location) - called when this object receives
                        another object

     at_traverse(traversing_object, source_loc) - (exit-objects only)
                              handles all moving across the exit, including
                              calling the other exit hooks. Use super() to retain
                              the default functionality.
     at_post_traverse(traversing_object, source_location) - (exit-objects only)
                              called just after a traversal has happened.
     at_failed_traverse(traversing_object)      - (exit-objects only) called if
                       traversal fails and property err_traverse is not defined.

     at_msg_receive(self, msg, from_obj=None, **kwargs) - called when a message
                             (via self.msg()) is sent to this obj.
                             If returns false, aborts send.
     at_msg_send(self, msg, to_obj=None, **kwargs) - called when this objects
                             sends a message to someone via self.msg().

     return_appearance(looker) - describes this object. Used by "look"
                                 command by default
     at_desc(looker=None)      - called by 'look' whenever the
                                 appearance is requested.
     at_get(getter)            - called after object has been picked up.
                                 Does not stop pickup.
     at_drop(dropper)          - called when this object has been dropped.
     at_say(speaker, message)  - by default, called if an object inside this
                                 object speaks

    """

    pass




class SbObject(DefaultObject):
    """
    Base object for everything in saiberponk
    """

    useSlot = WieldLocation.BACKPACK
    size = AttributeProperty(1,autocreate=False)
    value = AttributeProperty(0,autocreate=False)
    objType = ObjType.GEAR

    
    def at_object_creation(self):
        for objtypeElem in make_iter(self.objType):
            self.tags.add(objtypeElem.value, category="objType")

    
    def get_display_header(self, looker, **kwargs):
        """The top of the description"""
        return ""

    def get_display_desc(self,looker,**kwargs):
        return get_obj_stats(self,owner=looker)
    
    # Saiberponk commands
    
    def isObjType(self,objtype:ObjType):
        return objtype.value in make_iter(self.objType)

    def preUse(self,*args,**kwargs):
        return True

    def use(self,*args,**kwargs):
        pass

    def postUse(self,*args,**kwargs):
        pass

    def getHelp(self):
        return "Pas d'aide pour cet objet"
    
class SbQuest(SbObject):
    objType = ObjType.QUEST

class SbTreasure(SbObject):
    objType = ObjType.CREDITUBE
    value = AttributeProperty(100,autocreate=False)

class SbConsumable(SbObject):
    objType = ObjType.CONSUMABLE
    value = AttributeProperty(0.25,autocreate=False)
    uses = AttributeProperty(1,autocreate=False)

    def preUse(self,user,target=None,*args,**kwargs):
        if target and user.location != target.location:
            user.msg("Vous n'êtes pas assez proche de la cible !")
            return False
        if self.uses <= 0:
            user.msg(f"|w{self.key} est vide.|n")
            return False
    
    def use(self,user,*args,**kwargs):
        pass

    def postUse(self,user,*args,**kwargs):
        self.uses -= 1
        if self.uses <= 0:
            user.msg(f"|w{self.key} est vide.|n")
            self.delete()


class SbWeapon(SbObject):
    objType = ObjType.WEAPON
    useSlot = WieldLocation.RIGHT_HAND
    size = AttributeProperty(3,autocreate=False)
    value = AttributeProperty(0,autocreate=False)
    state = AttributeProperty(3,autocreate=False)
    weaponType = WeaponType.RANGED
    traumaDie = AttributeProperty("1d6",autocreate=False)
    damageDie = AttributeProperty("1d6",autocreate=False)


    def get_display_name(self,looker=None,**kwargs):
        stateDesc = ""
        if self.state is not None:
            if self.state <= 0:
                stateDesc = "|r(cassé)|n"
            elif self.state < 2:
                stateDesc = "|y(endommagé)|n"
            elif self.state < 3:
                stateDesc = "|Y(eraflé)|n"
            else:
                stateDesc = "|G(neuf)|n"

        return super().get_display_name(looker=looker,**kwargs) + stateDesc

    def preUse(self,user,target=None,*args,**kwargs):
        if target and user.location != target.location:
            user.msg("Vous n'êtes pas assez prêt de la cible !")
            return False
        if self.state is not None and self.state <= 0:
            user.msg(f"{self.get_display_name(user)} est cassé et ne peut pas être utilisé")
            return False
        return super().preUse(user,target=target,*args,**kwargs)
    
    def use(self,attacker,target,*args,**kwargs):
        location = attacker.location
        
        isHit:bool = False
        result = dice.roll("1d20")
        if result == 1:
            isHit = False
        elif result == 20:
            isHit = True
        else:
            if self.weaponType == WeaponType.RANGED:
                hitRoll = result + attacker.traits[Stat.DEX].mod + attacker.traits[Skill.TIR].value
                if hitRoll >= target.helper[CombatMixin.RGARMORCLASS]:
                    isHit = True
                else:
                    isHit = False
            elif self.weaponType == WeaponType.CLOSEQUARTER:
                #TODO:Modify to take care of CAC and FRP
                hitRoll = result + attacker.traits[Stat.FOR].mod + attacker.traits[Skill.CAC].value
                if hitRoll >= target.helper[CombatMixin.CQDARMORCLASS]:
                    isHit = True
                else:
                    isHit = False
        location.msg_contents(
            f"$You() $conj(attack) $You({target.key}) with {self.key}",
            from_obj=attacker,
            mapping={target.key: target},
            )
        if isHit:
            attacker.msg("Vous touchez !")
            target.msg("Vous êtes touché")
            #TODO: Implement Traumatic Hit handling
            #TODO: Implement Shock handling
            damageResult = dice.roll(self.damageDie)
            message = f" $You() $conj(hit) $You({target.key}) for |r{damageResult}|n dégats!"
            location.msg_contents(message, from_obj=attacker, mapping={target.key: target})
            target.atDamage(damageResult)
        else:
            # A miss
            message = f" $You() $conj(miss) $You({target.key})."
            if result == 1:
                message += ".. it's a |rcritical miss!|n, damaging the weapon."
                if self.state is not None:
                    self.state -= 1
            location.msg_contents(message, from_obj=attacker, mapping={target.key: target})

    def postUse(self,user,*args,**kwargs):
        if self.state is not None and self.state <= 0:
            user.msg(f"|r{self.get_display_name(user)} se casse et ne peut plus être utilisé(e) !")

class SbWeaponBareHands(SbWeapon):
    """
    This is a dummy-class loaded when you wield no weapons. We won't create any db-object for it.

    """
    objType = ObjType.WEAPON
    key = "Mains nues"
    useSlot = WieldLocation.RIGHT_HAND
    weaponType = WeaponType.CLOSEQUARTER
    damageDie = "1d2"
    traumaDie = "1d6"
    state = None  # let's assume fists are always available ...


    def getBareHands():
        """
        Get the bare-hands singleton object.

        Returns:
            WeaponBareHands
        """
        global _BARE_HANDS

        if not _BARE_HANDS:
            _BARE_HANDS = search_object("Mains nues", typeclass=SbWeaponBareHands).first()
        if not _BARE_HANDS:
            _BARE_HANDS = create_object(SbWeaponBareHands, key="Mains nues")
        return _BARE_HANDS


class SbArmor(SbObject):
    objType = ObjType.ARMOR
    useSlot = WieldLocation.BODY
    size = AttributeProperty(3,autocreate=False)
    value = AttributeProperty(0,autocreate=False)
    state = AttributeProperty(3,autocreate=False)
    damageSoak = AttributeProperty(0,autocreate=False)
    rangedAC = AttributeProperty(10,autocreate=False)
    closequarterAC = AttributeProperty(10,autocreate=False)


class SbHelmet(SbObject):
    objType = ObjType.HELMET
    useSlot = WieldLocation.HEAD
    size = AttributeProperty(3,autocreate=False)
    value = AttributeProperty(0,autocreate=False)
    state = AttributeProperty(3,autocreate=False)

