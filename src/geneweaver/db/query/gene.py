"""Generate SQL queries to get Gene information."""
from typing import List, Optional, Tuple

from geneweaver.core.enum import GeneIdentifier, Species
from geneweaver.core.mapping import AON_ID_TYPE_FOR_SPECIES
from geneweaver.db.utils import format_sql_fields, limit_and_offset
from psycopg.sql import SQL, Composed

GENE_FIELDS_MAP = {
    "ode_gene_id": "id",
    "ode_ref_id": "reference_id",
    "gdb_id": "gene_database",
    "sp_id": "species",
    "ode_pref": "preferred",
    "ode_date": "date",
}

GENE_FIELDS = format_sql_fields(GENE_FIELDS_MAP, query_table="gene")


def get(
    gene_id: Optional[int] = None,
    reference_id: Optional[str] = None,
    gene_database: Optional[GeneIdentifier] = None,
    species: Optional[Species] = None,
    preferred: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Tuple[Composed, dict]:
    """Create a psycopg query to Get genes from the database.

    :param gene_id: The id of the gene to get.
    :param reference_id: The reference id to search for.
    :param gene_database: The gene database to search for.
    :param species: The species to search for.
    :param preferred: Whether to search for preferred genes.
    :param limit: The limit of results to return.
    :param offset: The offset of results to return.

    :return:  A query (and params) that can be executed on a cursor.
    """
    params = {}
    query = SQL("SELECT") + SQL(",").join(GENE_FIELDS) + SQL("FROM gene")

    filtering = []

    if gene_id:
        filtering.append(SQL("ode_gene_id = %(gene_id)s"))
        params["gene_id"] = gene_id

    if reference_id:
        filtering.append(SQL("ode_ref_id = %(ref_id)s"))
        params["ref_id"] = reference_id

    if gene_database:
        filtering.append(SQL("gdb_id = %(gene_db_id)s"))
        params["gene_db_id"] = int(gene_database)

    if species:
        filtering.append(SQL("sp_id = %(species_id)s"))
        params["species_id"] = int(species)

    if preferred is not None:
        filtering.append(SQL("ode_pref = %(preferred)s"))
        params["preferred"] = preferred

    if len(filtering) > 0:
        query += SQL("WHERE") + SQL(" AND ").join(filtering)

    query = limit_and_offset(query, limit, offset).join(" ")

    return query, params


def mapping(
    source_ids: List[str],
    target_gene_id_type: GeneIdentifier,
) -> Tuple[Composed, dict]:
    """Create a query to get a list of gene IDs in an alternate identifier type.

    :param source_ids: The list of gene IDs to map.
    :param target_gene_id_type: The gene identifier type to map to.
    :return: A query (and params) that can be executed on a cursor.
    """
    params = {}
    query = (
        SQL("SELECT g1.ode_ref_id, g2.ode_ref_id")
        + SQL("FROM gene g1 JOIN gene g2")
        + SQL("ON g1.ode_gene_id = g2.ode_gene_id")
        + SQL("AND g1.ode_ref_id != g2.ode_ref_id")
        + SQL("AND g1.sp_id = g2.sp_id")
        + SQL("WHERE g1.ode_ref_id = ANY(%(source_ids)s)")
        + SQL("AND g2.gdb_id = %(target_gene_id_type)s")
    ).join(" ")
    params["source_ids"] = source_ids
    params["target_gene_id_type"] = int(target_gene_id_type)
    return query, params


def aon_mapping(
    source_ids: List[str],
    source_species: Species,
) -> Tuple[Composed, dict]:
    """Create a query to get a list of gene IDs the AON preferred identifier type.

    :param source_ids: The list of gene IDs to map.
    :param source_species: The species to map from.
    :return: A query (and params) that can be executed on a cursor.
    """
    target_gene_id_type = AON_ID_TYPE_FOR_SPECIES[source_species]
    return mapping(source_ids, target_gene_id_type)
