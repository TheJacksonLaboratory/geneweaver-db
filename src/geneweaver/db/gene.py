"""Database interaction code relating to Gene IDs."""
from typing import List, Optional

from psycopg import Cursor


def id_types(cursor: Cursor, species_id: Optional[int] = None) -> List:
    """Get all the Gene ID types from the database.

    :param cursor: The database cursor.
    :param species_id: Limit to additional species other than mouse

    :return: list of results using `.fetchall()`
    """
    if species_id is None:
        cursor.execute("""SELECT * FROM genedb ORDER BY gdb_id;""")
    else:
        cursor.execute(
            """SELECT * FROM genedb
            WHERE sp_id=0 OR sp_id=%(sp_id)s
            ORDER BY gdb_id;""",
            {"sp_id": species_id},
        )

    return cursor.fetchall()
