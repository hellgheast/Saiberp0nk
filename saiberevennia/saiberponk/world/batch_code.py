# HEADER

from evennia import create_object, search_object
from typeclasses.rooms import Room,SbRoom
from typeclasses.exits import Exit
from evennia import DefaultObject
from typeclasses.objects import SbWeapon,SbObject


# CODE

# Create a Room and make an exit to another one.
caller.msg(f"|[500Debut de construction de monde..|n")

# Croisement
Croisement = create_object(SbRoom,key="Croisement",nohome = True)
Croisement.db.desc = "|wUn croisement mal |=uéclairé|n."

# Déchéterie
Déchéterie = create_object(SbRoom, key="Déchéterie")
Déchéterie.db.desc = "Un amas de |140déchets|n, mélangés à des véhicules couvert |510 de rouille|n.."
exit = create_object(Exit, key="nord", aliases=["n"],location=Croisement, destination=Déchéterie)
exit2 = create_object(Exit, key="sud", aliases=["s"],location=Déchéterie, destination=Croisement)

# Magasin
Magasin = create_object(SbRoom,key="Magasin")
Magasin.db.desc = "Un |540magasin|n mal entretenu, couvert |yd'affiches|n, affichant les publicités en Tridéo."
exit3 = create_object(Exit, key="est", aliases=["e"],location=Croisement, destination=Magasin)
exit4 = create_object(Exit, key="ouest", aliases=["o"],location=Magasin, destination=Croisement)
# Création d'une arme
sg400 = create_object(SbWeapon,key="sg400",location=Magasin)
sg400.db.desc = "Une |500arme|n basique, fonctionnelle."
# Création d'une table
table = create_object(SbObject,key="table",location=Magasin)
table.db.desc = "Une table en |350plastique|n usée.."

caller.msg(f"|[500Fin de construction de monde..|n")