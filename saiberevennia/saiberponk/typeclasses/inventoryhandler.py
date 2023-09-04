from evennia.utils.utils import inherits_from
from module.enums import WieldLocation, Stat
from typeclasses.objects import SbObject, SbWeapon, SbWeaponBareHands
from typing import Dict, Any, List,Tuple


class InventoryError(TypeError):
    pass


class InventoryHandler:
    saveAttribute = "inventorySlots"

    def __init__(self, character) -> None:
        self.character = character
        self.load()

    def load(self):
        self.slots: Dict[WieldLocation, Any] = self.character.attributes.get(
            self.saveAttribute,
            category="inventory",
            default={
                str(WieldLocation.LEFT_HAND): None,
                str(WieldLocation.RIGHT_HAND): None,
                str(WieldLocation.TWO_HANDS): None,
                str(WieldLocation.HEAD): None,
                str(WieldLocation.BODY): None,
                str(WieldLocation.LEGS): None,
                str(WieldLocation.BACKPACK): [],
            },
        )
        self.slots[WieldLocation.BACKPACK] = [
            obj for obj in self.slots[WieldLocation.BACKPACK] if obj and obj.id
        ]


    def save(self):
        self.character.attributes.add(
            self.saveAttribute, self.slots, category="inventory"
        )

    @property
    def maxWeight(self):
        # Refactor and output maxCW from helper
        return self.character.helper.maxCW

    def currentWeight(self):
        slots = self.slots
        wieldWeight = sum(
            [
                getattr(slotobj, "size", 0) or 0
                for slot, slotobj in slots.items()
                if slot is not WieldLocation.BACKPACK
            ]
        )
        backpackWeight = sum(
            [
                getattr(slotobj, "size", 0) or 0
                for slotobj in slots[WieldLocation.BACKPACK]
            ]
        )
        return wieldWeight + backpackWeight

    @property
    def armor(self) -> Tuple[int,int]:
        rangedAC: int = (
            sum(
                getattr(self.slots[WieldLocation.BODY], "rangedAC", 10),
                getattr(self.slots[WieldLocation.HEAD], "rangedAC", 0),
            ),
        )
        closequaterAC: int = sum(
            getattr(self.slots[WieldLocation.BODY], "closequarterAC", 10),
            getattr(self.slots[WieldLocation.HEAD], "closequarterAC", 0),
        )
        return rangedAC, closequaterAC

    @property
    def weapons(self) -> List[SbWeapon]:
        weaponsList: List[SbWeapon] = []
        if self.slots[WieldLocation.TWO_HANDS] != None:
            weaponsList = [self.slots[WieldLocation.TWO_HANDS]]
        else:
            # Check left and right hand
            if isinstance(self.slots[WieldLocation.LEFT_HAND], SbWeapon):
                weaponsList = [self.slots[WieldLocation.LEFT_HAND]]
            if isinstance(self.slots[WieldLocation.RIGHT_HAND], SbWeapon):
                weaponsList.extend([self.slots[WieldLocation.RIGHT_HAND]])
            # If no weapon has been found, we use our bare fists.
            if len(weaponsList) == 0:
                weaponsList = [SbWeaponBareHands.getBareHands()]
        return weaponsList

    def displayCarryUsage(self):
        return f"|b{self.currentWeight()}/{self.maxWeight} kgs"

    def displayLoadout(self) -> str:
        """
        Shows the currently equipped material
        """
        weaponStr = "Tu te bats à main nues"
        armorStr = "Tu ne portes pas d'armure"
        helmetStr = "et pas de casque."
        #TODO:Add something for the legs
        twoHands = self.slots[WieldLocation.TWO_HANDS]
        if twoHands:
            weaponStr = f"Tu portes {twoHands} à deux mains"
        else:
            leftHand = self.slots[WieldLocation.LEFT_HAND]
            rightHand = self.slots[WieldLocation.RIGHT_HAND]
            if isinstance(leftHand, SbWeapon) and isinstance(rightHand,SbWeapon):
                weaponStr = f"Tu portes {leftHand} dans ta main gauche et {rightHand} dans ta main droite."
            elif isinstance(leftHand,SbWeapon):
                weaponStr = f"Tu portes {leftHand} dans ta main gauche."
            elif isinstance(rightHand,SbWeapon):
                weaponStr = f"Tu portes {rightHand} dans ta main droite."
        armor = self.slots[WieldLocation.BODY]
        if armor:
            armorStr = f"Tu portes {armor}"
        helmet = self.slots[WieldLocation.HEAD]
        if helmet:
            helmetStr = f"et {helmet} sur ta tête"
        
        return f"{weaponStr}\n{armorStr} {helmetStr}"
    
    def displayBackpack(self) -> str:
        backpack = self.slots[WieldLocation.BACKPACK]
        if not backpack:
            return "Le sac à dos est vide."
        out = []
        for item in backpack:
            out.append(f"{item.key} [|b{item.size}|n] kg")
        return "\n".join(out)

    def validateSlotUsage(self, obj):
        if not inherits_from(obj, SbObject):
            raise InventoryError(f"{obj.key} n'est pas équipable.")

        size = obj.size
        maxWeight = self.maxWeight
        currentWeight = self.currentWeight()
        if currentWeight + size > maxWeight:
            remainingWeight = maxWeight - currentWeight
            raise InventoryError(
                f"Surcharge {remainingWeight} kg disponible"
                f"{obj.key} à besoin de {size} kg"
            )
        return currentWeight + size <= maxWeight

    def findObjSlot(self,obj):
        for item,slot in self.all():
            if obj == item:
                return slot
    
    def getWieldableObjects(self):
        return [obj for obj in self.slots[WieldLocation.BACKPACK] if obj and obj.id and obj.useSlot in [WieldLocation.LEFT_HAND,WieldLocation.RIGHT_HAND,WieldLocation.TWO_HANDS] ]

    def getWearableObjects(self):
        return [obj for obj in self.slots[WieldLocation.BACKPACK] if obj and obj.id and obj.useSlot in [WieldLocation.HEAD,WieldLocation.BODY,WieldLocation.LEGS] ]

    def getUsableObjects(self):
        return [
            obj for obj in self.slots[WieldLocation.BACKPACK] if obj and obj.id and obj.preUse(self.character)
        ]

    def add(self, obj):
        if self.validateSlotUsage(obj):
            self.slots[WieldLocation.BACKPACK].append(obj)
            self.character.helper.cw += obj.size
            self.save()

    def remove(self, slotObj):
        ret = []
        #import pdb; pdb.set_trace()
        if isinstance(slotObj, WieldLocation):
            if slotObj is WieldLocation.BACKPACK:
                # empty entire backpack
                ret.extend(self.slots[slotObj])
                self.slots[slotObj] = []
            else:
                ret.append(self.slots[slotObj])
                self.slots[slotObj] = None
        elif slotObj in self.slots.values():
            for slot, elem in self.slots.items():
                if elem is slotObj:
                    self.slots[slot] = None
                    ret.append(slotObj)
        elif slotObj in self.slots[WieldLocation.BACKPACK]:
            try:
                self.slots[WieldLocation.BACKPACK].remove(slotObj)
                ret.append(slotObj)
            except ValueError:
                pass
        if ret:
            removedWeight = 0
            for elem in ret:
                removedWeight += getattr(elem, "size", 0)
            self.character.helper.cw -= removedWeight
            self.save()
        return ret

    def move(self, obj):
        # We remove the object to be sure to not duplicate it
        self.remove(obj)
        self.validateSlotUsage(obj)
        toBackpack = []
        # Which slot does this object uses
        useSlot = getattr(obj, "useSlot", WieldLocation.BACKPACK)
        #self.character.msg(f"move: {useSlot}")
        if useSlot is WieldLocation.TWO_HANDS:
            # If we have anything in right and left hand we remove it
            toBackpack = [
                self.slots[WieldLocation.RIGHT_HAND],
                self.slots[WieldLocation.LEFT_HAND],
            ]
            self.slots[WieldLocation.RIGHT_HAND] = None
            self.slots[WieldLocation.LEFT_HAND] = None
            self.slots[useSlot] = obj
        elif useSlot in [WieldLocation.RIGHT_HAND, WieldLocation.LEFT_HAND]:
            # We move the dual hand weapon back to backpack
            toBackpack = [self.slots[WieldLocation.TWO_HANDS]]
            self.slots[WieldLocation.TWO_HANDS] = None
            self.slots[useSlot] = obj
        elif useSlot is WieldLocation.BACKPACK:
            toBackpack = [obj]
            self.character.msg("In bkp")
        else:
            # for head,body and legs
            toBackpack = [self.slots[useSlot]]
            self.slots[useSlot] = obj

        for backpackObj in toBackpack:
            # backpackObj can be None that we moved around..
            if backpackObj:
                self.slots[WieldLocation.BACKPACK].append(backpackObj)

        self.save()

    def all(self, onlyObj=False):
        """Return a list of all items in inventory"""
        inventory = [
            (self.slots[enum], enum)
            for enum in WieldLocation.enumList()
            if enum != WieldLocation.BACKPACK
        ]
        inventory.extend(
            [
                (item, WieldLocation.BACKPACK)
                for item in self.slots[WieldLocation.BACKPACK]
            ]
        )
        if onlyObj:
            return [obj for obj, _ in inventory if obj]
        return inventory
