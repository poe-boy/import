"""
Data access for PoEBoy import.
"""

import psycopg2
import psycopg2.extras

CONN = None


def ensure_connection():
    """
    Ensure we have a connection per import. (Lazy connection)
    """

    global CONN

    if CONN is None:
        CONN = psycopg2.connect(
            host='localhost', database='poeboy', user='postgres')


def get_cursor():
    """
    Return predefined cursor.
    """

    return CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)


def get_next_change_id():
    """
    Returns the next change id.
    """

    next_change_id = None

    ensure_connection()

    with get_cursor() as cur:
        cur.execute('select * from next_change_id;')
        record = cur.fetchone()
        CONN.commit()

    if record is not None:
        next_change_id = record['id']

    return next_change_id


def update_next_change_id(next_change_id):
    """
    Updates or creates the next change id.
    """

    ensure_connection()

    existing = get_next_change_id()

    with get_cursor() as cur:
        if existing is None:
            cur.execute(
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
            cur.execute(
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
