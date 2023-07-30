from typing import Dict, List
from module.enums import Stat,WeaponType

_OBJ_STATS = """
|c{key}|n
Valeur: ~|y{value}|n C$ {carried}

{desc}

Taille: |w{size}|n, Emplacement: |w{use_slot_name}|n
État: |w{state}|n, Utilisation: |w{uses}|n
{weaponType} |w{attack_type_name}|n contre |w{defense_type_name}|n
Dé de dégâts: |w{damageDie}|n
""".strip()


def get_obj_stats(obj, owner=None): 
    """ 
    Get a string of stats about the object.
    
    Args:
        obj (Object): The object to get stats for.
        owner (Object): The one currently owning/carrying `obj`, if any. Can be 
            used to show e.g. where they are wielding it.
    Returns:
        str: A nice info string to display about the object.
     
    """
    #TODO: Handle args and kwargs

    carried = ""
    if owner:
        pass

    weaponType = getattr(obj,"weaponType",None)
    if weaponType:
        if weaponType == WeaponType.RANGED:
            attack_type_name = Stat.DEX
            weaponTypedesc = f"Arme à {WeaponType.RANGED}"
        else:
            attack_type_name = Stat.FOR
            weaponTypedesc = f"Arme de {WeaponType.CLOSEQUARTER}"

    return _OBJ_STATS.format(
        key=obj.key, 
        value=obj.value, 
        carried="[Pas porté]", 
        desc=obj.db.desc, 
        size=obj.size,
        state=getattr(obj,"state","N/A"),
        uses=getattr(obj,"uses","N/A"),
        use_slot_name="Sac à dos",
        weaponType=weaponTypedesc if weaponType else "",
        attack_type_name=attack_type_name.value if weaponType else "",
        defense_type_name="Armure" if weaponType else "",
        damageDie=getattr(obj,"damageDie","Aucun"),
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


