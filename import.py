#!/usr/bin/python

"""
Import stash tab data data from PoE.
"""

import sys
import threading
import requests
import data

ARGS = sys.argv[1:]


def get_next_change_id():
    """
    Gets the next change id from poe.ninja or the database.
    """

    next_change_id = None

    args_length = len(ARGS)

    if args_length > 0 and ARGS[0] == 'true':
        res = requests.get('http://poe.ninja/api/Data/GetStats')

        next_change_id = res.json()['next_change_id']
    else:
        next_change_id = data.get_next_change_id()

    return next_change_id


def request_stash_tabs(next_change_id=None):
    """
    Calls the stash tab API and returns the data.
    """

    res = requests.get(
        'http://pathofexile.com/api/public-stash-tabs?id={0}'.format(next_change_id))

    return res.json()


def map_properties(property_list, prop_type):
    """
    Maps properties/requirements for an item.
    """

    mapped_property_list = []

    for p in property_list:
        has_len = 'values' in p and len(p['values']) > 0
        has_2 = has_len and len(p['values']) > 1

        prop = {
            'name': p['name'],
            'value_1': p['values'][0][0] if has_len is True else None,
            'value_type_1': p['values'][0][1] if has_len is True else None,
            'value_2': p['values'][1][0] if has_2 is True else None,
            'value_type_2': p['values'][1][1] if has_2 is True else None,
            'display_mode': p['displayMode'],
            'type': prop_type,
            'progress': p['progress'] if 'progress' in p else None,
            'property_type': p['type'] if 'type' in p else None,
            'is_additional': p['isAdditional'] if 'isAdditional' in p else None
        }

        mapped_property_list.append(prop)

    return mapped_property_list


def map_items(item_list):
    """
    Maps items.
    """

    mapped_list = []

    for i in item_list:
        item = {
            'verified': i['verified'],
            'dimensions': {
                'w': i['w'],
                'h': i['h']
            },
            'ilvl': i['ilvl'],
            'icon': i['icon'],
            'league': i['league'],
            'item_id': i['id'],
            'name': i['name'],
            'type_line': i['typeLine'],
            'identified': i['identified'],
            'corrupted': i['corrupted'],
            'locked_to_character': i['lockedToCharacter'],
            'note': i['note'] if 'note' in i else None,
            'explicit_mods': ''.join(i['explicitMods']) if 'explicitMods' in i else None,
            'enchant_mods': ''.join(i['enchantMods']) if 'enchantMods' in i else None,
            'crafted_mods': ''.join(i['craftedMods']) if 'craftedMods' in i else None,
            'flavour_text': ''.join(i['flavourText']) if 'flavourText' in i else None,
            'frame_type': i['frameType'],
            'stash_position': {
                'x': i['x'],
                'y': i['y']
            },
            'inventory_id': i['inventoryId'],
            'properties': map_properties(i['properties'], 'property') if 'properties' in i else [],
            'requirements': map_properties(i['requirements'], 'requirement') if 'requirements' in i else []
        }

        mapped_list.append(item)

    return mapped_list


def map_stash_data(stash_data):
    """
    Maps response data to a usable data structure.
    """

    next_change_id = stash_data['next_change_id']

    stash_list = []

    for stash in stash_data['stashes']:
        mapped_account = {
            'name': stash['accountName'],
            'last_character_name': stash['lastCharacterName']
        }

        mapped_stash = {
            'account_id': None,
            'stash_id': stash['id'],
            'stash': stash['stash'],
            'type': stash['stashType']
        }

        mapped_item_list = map_items(stash['items'])

        stash_list.append({
            'account': mapped_account,
            'stash': mapped_stash,
            'item_list': mapped_item_list
        })

    return next_change_id, stash_list


def main(next_change_id=None):
    """
    Return the pathname of the KOS root directory.
    """

    if next_change_id is None:
        next_change_id = get_next_change_id()

    print('processing change id:', next_change_id or 'first')

    stash_data = request_stash_tabs(next_change_id)

    mapped = map_stash_data(stash_data)

    if next_change_id is not None:
        data.update_next_change_id(next_change_id)

    # if returned next change id doesn't match the one we started with, run again
    if next_change_id != mapped[0]:
        threading.Timer(5, main, [mapped[0]]).start()


if __name__ == '__main__':
    main()
