# Saiberponk
A simple but funny project !

# Shitposters
Thanks for all the Mumble team for this experiment
Also big thanks to Natalie from evennia discord and also SirBacon from Mumble for the awesome support !

# Tech stack
Now:
## Frontend
VanillaJS
GoldenLayout
## Backend
Django
Evennia
https://github.com/aparrish/pytracery
# Maybe Future tech stack:
Pixi.js
Agenda
https://github.com/propjockey/augmented-ui
Websockets
Vue.js
https://express-validator.github.io/docs/

# Docker change folder 
https://stackoverflow.com/a/66314636
# WSL2 fixing localhost access
https://docs.microsoft.com/en-us/windows/wsl/wsl-config
**Addtionnal note: save .wslconfig in CR+LF format ! OR IT DOESN'T WORK**

# Inspiration
Sindome : https://github.com/JavaChilly/dome-client.js
for giving me the will to try it myself

WrittenRealms : https://github.com/teebes/herald for the good advices provided and showing me what is possible with Vue.js

# Ressources, documentation
https://github.com/sevenecks/lambda-moo-programming

# Useful commands
sudo mongod --dbpath ./test/db
mongosh
mongoose

# Useful evennia commands
``type/update
update character
update me
delete the server evennia.db3
evennia migrate
evennia start
voir le server.log pour les erreurs au démarrage
examine me est pratique

# Get attributes
https://www.evennia.com/docs/latest/Components/Attributes.html?highlight=attributehandler
https://www.evennia.com/docs/latest/Components/Objects.html
https://www.evennia.com/docs/latest/Components/Components-Overview.html
https://www.evennia.com/docs/latest/Components/Objects.html#changing-an-objects-appearance
https://www.evennia.com/docs/latest/Components/Exits.html
https://www.evennia.com/docs/latest/Components/Rooms.html
https://www.evennia.com/docs/latest/Components/Tags.html
https://www.evennia.com/docs/latest/Components/Prototypes.html
https://www.evennia.com/docs/latest/Components/Permissions.html
https://www.evennia.com/docs/latest/Components/Locks.html
https://www.evennia.com/docs/latest/Components/Commands.html#how-commands-actually-work
https://www.evennia.com/docs/latest/Evennia-API.html

# Set stuff from evennia
use `set` command
## Room creation
dig market:rooms.RandomRoom = market,back
>> py here.startEcho()
## Object creation
create Sg400:objects.SbWeapon

## Have builder
Need to add needed permissions to account and character !
pperm Builder
perm Builder
# update evennia in virtual env
pip install -e evennia
cd saiberponk
evennia migrate