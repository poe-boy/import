#!/usr/bin/python

"""
Import stash tab data data from PoE.
"""

import sys
import threading
import requests
import data

ARGS = sys.argv[1:]


def get_change_id():
    """
    Gets the next change id from poe.ninja or the database.
    """

    change_id = None

    args_length = len(ARGS)

    if args_length > 0 and ARGS[0] == 'true':
        res = requests.get('http://poe.ninja/api/Data/GetStats')

        change_id = res.json()['next_change_id']
    else:
        change_id = data.get_next_change_id()

    return change_id


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
            'progress': p.get('progress', None),
            'property_type': p.get('type', None),
            'is_additional': p.get('isAdditional', None)
        }

        mapped_property_list.append(prop)

    return mapped_property_list


def map_items(item_list, stash_id):
    """
    Maps items.
    """

    mapped_list = []

    for i in item_list:
        item = {
            # our mapping property later
            'stash_id': stash_id,
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
            'explicit_mods': ''.join(i.get('explicitMods', [])) or None,
            'enchant_mods': ''.join(i.get('enchantMods', [])) or None,
            'crafted_mods': ''.join(i.get('craftedMods', [])) or None,
            'flavour_text': ''.join(i.get('flavourText', [])) or None,
            'frame_type': i['frameType'],
            'stash_position': {
                'x': i['x'],
                'y': i['y']
            },
            'inventory_id': i['inventoryId'],
            'properties': map_properties(i.get('properties', []), 'property'),
            'requirements': map_properties(i.get('requirements', []), 'requirement')
        }

        mapped_list.append(item)

    return mapped_list


def map_stash_data(stash_data):
    """
    Maps response data to a usable data structure.
    """

    next_change_id = stash_data['next_change_id']

    account_list = []
    stash_list = []
    item_list = []

    for stash in stash_data['stashes']:
        # add unique accounts by `accountName`
        if not any(a['name'] == stash['accountName'] for a in account_list):
            account_list.append({
                'name': stash['accountName'],
                'last_character_name': stash['lastCharacterName']
            })

        # add unique stashes by stash `id`
        if not any(s['stash_id'] == stash['id'] for s in stash_list):
            stash_list.append({
                # our mapping property later
                'account_name': stash['accountName'],
                'stash_id': stash['id'],
                'stash': stash['stash'],
                'type': stash['stashType']
            })

            item_list = map_items(stash['items'], stash['id'])

    return {
        'account_list': account_list,
        'stash_list': stash_list,
        'item_list': item_list
    }


def main(change_id=None):
    """
    Main process.
    """

    if change_id is None:
        change_id = get_change_id()

    print('processing change id:', change_id or 'first')

    response = request_stash_tabs(change_id)

    next_change_id = response['next_change_id']

    # before we do anything,
    if change_id == next_change_id:
        print('change id is identical')
        threading.Timer(5, main, [next_change_id]).start()
    else:
        mapped = map_stash_data(response)

        print('updating next change id')
        data.update_next_change_id(next_change_id)

        threading.Timer(5, main, [next_change_id]).start()


if __name__ == '__main__':
    main()
