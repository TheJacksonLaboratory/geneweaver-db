"""Database code for interacting with Publication table."""
from psycopg import Cursor


def get_publication_by_pubmed_id(cursor: Cursor, pmid: int) -> dict:
    """Get a publication by PMID."""
    cursor.execute(
        """
        SELECT * FROM publication
        WHERE pub_pubmed = %s
        """,
        (pmid,),
    )
    return cursor.fetchone()


def get_publications_by_pubmed_ids(cursor: Cursor, pmids: list[int]) -> list[dict]:
    """Get publications by a list of PMIDs."""
    cursor.execute(
        """
        SELECT * FROM publication
        WHERE pub_pubmed = ANY(%s)
        """,
        (pmids,),
    )
    return cursor.fetchall()
