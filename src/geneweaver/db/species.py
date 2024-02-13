"""Species database functions."""
from typing import List, Optional

from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.db.utils import format_sql_fields
from psycopg import Cursor, rows
from psycopg.sql import SQL

SPECIES_FIELD_MAP = {
    "sp_id": "id",
    "sp_name": "name",
    "sp_taxid": "taxonomic_id",
    "sp_ref_gdb_id": "reference_gene_identifier",
}


SPECIES_FIELDS = format_sql_fields(SPECIES_FIELD_MAP, query_table="species")


def get(
    cursor: Cursor,
    taxonomic_id: Optional[int] = None,
    reference_gene_db_id: Optional[GeneIdentifier] = None,
    species: Optional[Species] = None,
) -> List:
    query = SQL("SELECT") + SQL(",").join(SPECIES_FIELDS) + SQL("FROM species")

    if species:
        query += SQL("WHERE sp_id = %(species_id)s")

    if taxonomic_id:
        query += SQL("WHERE sp_taxid = %(taxonomic_id)s")

    if reference_gene_db_id:
        query += SQL("WHERE sp_ref_gdb_id = %(reference_gene_db_id)s")

    query = query.join(" ")

    cursor.execute(query, {"species_id": int(species)})

    return cursor.fetchall()


def get_by_id(
    cursor: Cursor,
    species: Species,
) -> Optional[rows.Row]:
    query = (
        SQL("SELECT")
        + SQL(",").join(SPECIES_FIELDS)
        + SQL("FROM species")
        + SQL("WHERE sp_id = %(species_id)s")
    )

    cursor.execute(query, {"species_id": int(species)})

    return cursor.fetchone()
