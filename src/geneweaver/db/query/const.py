"""Consts for query module."""

from geneweaver.db.utils import format_sql_fields
from psycopg.sql import SQL, Identifier, Placeholder

PUB_FIELD_MAP = {
    "pub_id": "id",
    "pub_authors": "authors",
    "pub_title": "title",
    "pub_abstract": "abstract",
    "pub_journal": "journal",
    "pub_volume": "volume",
    "pub_pages": "pages",
    "pub_month": "month",
    "pub_year": "year",
    "pub_pubmed": "pubmed_id",
}

PUB_FIELDS = format_sql_fields(PUB_FIELD_MAP, query_table="publication")

PUB_QUERY = SQL("SELECT") + SQL(",").join(PUB_FIELDS) + SQL("FROM publication")

PUB_INSERT_COLS = SQL(",").join(
    [Identifier(k) for k in PUB_FIELD_MAP.keys() if k != "pub_id"]
)
PUB_INSERT_VALS = SQL(",").join(
    [Placeholder(k) for k in PUB_FIELD_MAP.keys() if k != "pub_id"]
)
PUB_TSVECTOR = (Identifier("publication") + Identifier("pub_tsvector")).join(".")
