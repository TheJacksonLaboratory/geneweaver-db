"""Geneset thresholding database functions."""

from geneweaver.core.schema.score import GenesetScoreType
from geneweaver.db.query import threshold as threshold_query
from psycopg import Cursor


def set_geneset_threshold(
    cursor: Cursor,
    geneset_id: int,
    geneset_score_type: GenesetScoreType,
) -> None:
    """Update the threshold of a geneset and its values.

    :param cursor: An database cursor.
    :param geneset_id: The ID of the geneset to update.
    :param geneset_score_type: The score threshold to set.
    :return: Nothing.
    """
    cursor.execute(
        *threshold_query.set_geneset_threshold(geneset_id, geneset_score_type)
    )
    cursor.execute(
        *threshold_query.set_geneset_value_threshold(geneset_id, geneset_score_type)
    )
