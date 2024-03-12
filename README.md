# dicebot2
remaking my discord die bot on new python lib


# Goals

## Rolling
- ~~Advantage & Disadvantage~~
- ~~Roll~~, RollOne, ~~RollMulti~~
- ~~Old rolling system~~ - Removed
- Track initiative
- 
## User profiles
- Get all characters and have it autofill - partial, want to go back and make cleaner
- Profile info

## Characters 
- ~~unique user database~~ - done, using mongoDB
- character creating - Basics are done
- skill checks - Basics are done
- common dice patterns (make certain move and preload dice)
- Character descriptions
- 
## Database
- split mongoHandler into separate class to be command specific for cleaner clode
- Spell and attack tables
- Fill Spell and attack tables

## Spell and Attacks
- Find way to compile them all
- create new command catagory to handle

## Embed Handler
- Debating if this should be a class or not
  - Lifespan will only be in each function 
  - Its pretty simple already
  - Lacks protection and error handling, all calls are with 

## Other 
- Modal Dialogs
- Maybe make this into other scopes down the line?

## Info
- pull from 5e.tools
## credits/lore
-  Add character lore or global dictionaries
- add notes