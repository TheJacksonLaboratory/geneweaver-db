"""Generate SQL queries to get Species information."""

from typing import Optional, Tuple

from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.db.utils import format_sql_fields
from psycopg.sql import SQL, Composed

SPECIES_FIELD_MAP = {
    "sp_id": "id",
    "sp_name": "name",
    "sp_taxid": "taxonomic_id",
    "sp_ref_gdb_id": "reference_gene_identifier",
}


SPECIES_FIELDS = format_sql_fields(SPECIES_FIELD_MAP, query_table="species")


def get(
    taxonomic_id: Optional[int] = None,
    reference_gene_db_id: Optional[GeneIdentifier] = None,
    species: Optional[Species] = None,
) -> Tuple[Composed, dict]:
    """Create a psycopg query to get species information from the database.

    :param taxonomic_id: The taxonomic id.
    :param reference_gene_db_id: The reference gene database id.
    :param species: The species id.

    :return: A query (and params) that can be executed on a cursor.
    """
    params = {}
    query = SQL("SELECT") + SQL(",").join(SPECIES_FIELDS) + SQL("FROM species")

    filters = []

    if species:
        filters.append(SQL("sp_id = %(species_id)s"))
        params["species_id"] = int(species)

    if taxonomic_id:
        filters.append(SQL("sp_taxid = %(taxonomic_id)s"))
        params["taxonomic_id"] = taxonomic_id

    if reference_gene_db_id:
        filters.append(SQL("sp_ref_gdb_id = %(reference_gene_db_id)s"))
        params["reference_gene_db_id"] = int(reference_gene_db_id)

    if len(filters) > 0:
        query += SQL("WHERE") + SQL("AND").join(filters)

    query = query.join(" ")

    return query, params
