"""Constants for search queries."""

from psycopg.sql import Identifier

SEARCH_COMBINED_COL = (
    Identifier("geneset_search") + Identifier("_combined_tsvector")
).join(".")
