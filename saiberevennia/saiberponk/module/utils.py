from typing import Dict, List
from module.enums import Stat

_OBJ_STATS = """
|c{key}|n
Valeur: ~|y{value}|n C$ {carried}

{desc}

Taille: |w{size}|n, Used from: |w{use_slot_name}|n
Qualité: |w{quality}|n, Utilisation: |w{uses}|n
Attacks using |w{attack_type_name}|n contre |w{defense_type_name}|n
Dé de dégâts: |w{damage_roll}|n
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
    return _OBJ_STATS.format(
        key=obj.key, 
        value=10, 
        carried="[Pas porté]", 
        desc=obj.db.desc, 
        size=1,
        quality=3,
        uses="infinie",
        use_slot_name="Sac à dos",
        attack_type_name=Stat.FOR.value,
        defense_type_name="Armure",
        damage_roll="1d6"
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


