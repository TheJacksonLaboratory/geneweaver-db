"""Constants for use in geneset queries."""

from geneweaver.db.query.publication import PUB_FIELD_MAP
from geneweaver.db.utils import format_sql_fields
from psycopg.sql import SQL, Identifier

GENESET_FIELDS_MAP = {
    "gs_id": "id",
    "usr_id": "user_id",
    "file_id": "file_id",
    "cur_id": "curation_id",
    "sp_id": "species_id",
    "gs_name": "name",
    "gs_abbreviation": "abbreviation",
    "pub_id": "publication_id",
    "gs_description": "description",
    "gs_count": "count",
    "gs_threshold_type": "score_type",
    "gs_threshold": "threshold",
    "gs_status": "status",
    "gs_gene_id_type": "gene_id_type",
    "gs_attribution": "attribution",
    "gs_created": "created",
    "gs_updated": "updated",
}

GENESET_FIELDS = format_sql_fields(GENESET_FIELDS_MAP, query_table="geneset")
PUB_FIELDS = format_sql_fields(
    PUB_FIELD_MAP, query_table="publication", resp_prefix="publication"
)
GENESET_TSVECTOR = (Identifier("geneset") + Identifier("gs_tsvector")).join(".")

COPY_GENESET_VALUES = SQL(
    """
                COPY geneset_value
                (gs_id,
                ode_gene_id,
                gsv_value,
                gsv_source_list,
                gsv_value_list,
                gsv_in_threshold,
                gsv_hits,
                gsv_date)
                FROM STDIN
                """
)
