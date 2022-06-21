# HEADER

from evennia import create_object, search_object
from typeclasses.rooms import Room
from typeclasses.exits import Exit
from evennia import DefaultObject

# CODE

# Create a Room and make an exit to another one.
caller.msg(f"Debut de construction de monde..")

cell_404 = create_object(Room,key="cell_404",nohome = True)
cell_404.db.desc = "|rUne cellule lugubre.."
room2 = create_object(Room, key="room2")
room2.db.desc = "|gUne porte de sortie.."
exit = create_object(Exit, key="out", location=cell_404, destination=room2)
exit2 = create_object(Exit, key="back", location=room2, destination=cell_404) 

caller.msg(f"Fin de construction de monde..")