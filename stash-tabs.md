# [Stash Tabs](https://pathofexile.gamepedia.com/Public_stash_tab_API)

Property       | Description | Type
-------------- | ----------- | ------------
next_change_id |             | string
stashes        | See below   | array[assoc]

## stashes

Property          | Description                                                                      | Type
----------------- | -------------------------------------------------------------------------------- | ------------
accountName       | account name the stash linked to                                                 | string
lastCharacterName | last character name of the player                                                | string
id                | unique stash id                                                                  | string
stash             | stash name                                                                       | string
stashType         | NormalStash/PremiumStash/QuadStash/EssenceStash/CurrencyStash (DivinationStash?) | string
items             | See below, items included in this stash                                          | array[assoc]
public            | public or not                                                                    | bool

## items

Property              | Description                                          | Type
--------------------- | ---------------------------------------------------- | ------------
verified              | bool                                                 |
w                     | slot width                                           | integer
h                     | slot height                                          | integer
ilvl                  | item level                                           | integer
icon                  | item picture art                                     | string
league                | Standard/Hardcore/                                   | string
id                    | item id, will change if you use currency on it       | string
sockets               | See below, array of sockets                          | array[assoc]
name                  | unique name                                          | string
typeLine              | item base type, mixed with affix name for magic/rare | string
identified            |                                                      | bool
corrupted             |                                                      | bool
lockedToCharacter     |                                                      | bool
note                  |                                                      | string
properties            | See below                                            | array[assoc]
requirements          | See below                                            | array[assoc]
explicitMods          | string                                               | array
implicitMods          | string                                               | array
enchantMods           | labyrinth mods                                       | string array
craftedMods           | master mods                                          | string array
flavourText           | string                                               | array
frameType             | See below                                            | integer
x                     | stash position x                                     | integer
y                     | stash position y                                     | integer
inventoryId           | slot                                                 | string
socketedItems         | See items                                            | array[assoc]
additionalProperties  | See properties                                       | array[assoc]
secDescrText          | second description text                              | string
descrText             | description text                                     | string
artFilename           | Divination Card                                      | string
duplicated            |                                                      | bool
maxStackSize          |                                                      | integer
nextLevelRequirements | See requirements                                     | array[assoc]
stackSize             |                                                      | integer
talismanTier          |                                                      | integer
utilityMods           | flask utility mods                                   | string array
support               |                                                      | bool
cosmeticMods          |                                                      | string array
prophecyDiffText      | prophecy difficulty text                             | string
prophecyText          |                                                      | string
isRelic               |                                                      | bool

## sockets

Property | Description                                                 | Type
-------- | ----------------------------------------------------------- | -------
group    | group id                                                    | integer
attr     | attribute, S=Strength, I=Intelligence, D=Dexterity, G=white | string

## properties/requirements

Property    | Description                               | Type
----------- | ----------------------------------------- | -------
name        |                                           | string
values      | array[0] is value, array[1] is valueTypes | array
displayMode | integer                                   |
type        | properties type                           | integer
progress    | additionalProperties's Experience         | integer

## valueTypes

Key | Description
--- | -----------------------
0   | white, or physical
1   | blue for modified value
4   | fire
5   | cold
6   | lightning
7   | chaos

## frameType

Key | Description
--- | ---------------
0   | normal
1   | magic
2   | rare
3   | unique
4   | gem
5   | currency
6   | divination card
7   | quest item
8   | prophecy
9   | relic