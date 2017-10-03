"""
Data access for PoEBoy import.
"""

import psycopg2
import psycopg2.extras

CONN = psycopg2.connect('dbname=poeboy user=postgres')

CUR = CONN.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)


def get_next_change_id():
    """
    Returns the next change id.
    """

    next_change_id = None

    CUR.execute('select * from next_change_id;')

    record = CUR.fetchone()

    if record is not None:
        next_change_id = record.id

    return next_change_id


def update_next_change_id(next_change_id):
    """
    Updates or creates the next change id.
    """

    existing = get_next_change_id()

    if existing is None:
        CUR.execute(
            '''
            insert into next_change_id (
                id,
                previous_id
            ) values (
                %s,
                %s
            );
            ''',
            (next_change_id, next_change_id)
        )
    else:
        CUR.execute(
            '''
            update
                next_change_id
            set
                id = %s,
                previous_id = id,
                updated_on = now();
            ''',
            (next_change_id,)
        )

    CONN.commit()
