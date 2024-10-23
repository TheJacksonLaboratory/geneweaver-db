"""Geneset thresholding database functions."""

from geneweaver.core.schema.score import GenesetScoreType
from geneweaver.db.query import threshold as threshold_query
from psycopg import AsyncCursor


async def user_can_set_threshold(
    cursor: AsyncCursor, user_id: int, geneset_id: int
) -> bool:
    """Check if a user can set the threshold of a geneset.

    :param cursor: An async database cursor.
    :param user_id: The ID of the user to check.
    :param geneset_id: The ID of the geneset to check.
    :return: True if the user can set the threshold, False otherwise.
    """
    await cursor.execute(*threshold_query.user_can_set_threshold(user_id, geneset_id))
    return bool(await cursor.fetchone())


async def set_geneset_threshold(
    cursor: AsyncCursor,
    user_id: int,
    geneset_id: int,
    geneset_score_type: GenesetScoreType,
) -> None:
    """Update the threshold of a geneset and its values.

    :param cursor: An async database cursor.
    :param user_id: The ID of the user.
    :param geneset_id: The ID of the geneset to update.
    :param geneset_score_type: The score threshold to set.
    :return: Nothing.
    """
    if not (await user_can_set_threshold(cursor, user_id, geneset_id)):
        raise ValueError("User cannot set threshold for geneset")

    await cursor.execute(
        *threshold_query.set_geneset_threshold(geneset_id, geneset_score_type)
    )
    await cursor.execute(
        *threshold_query.set_geneset_value_threshold(geneset_id, geneset_score_type)
    )
