"""Query functions related to thresholding and score type."""

from typing import Tuple

from geneweaver.core.schema.score import GenesetScoreType
from geneweaver.db.query import user
from psycopg.sql import SQL, Composed


def set_geneset_threshold(
    geneset_id: int,
    geneset_score_type: GenesetScoreType,
) -> Tuple[Composed, dict]:
    """Update the threshold of a geneset.

    After calling this query, the query in `update_geneset_value_threshold` should be
    called.

    :param geneset_id: The ID of the geneset to update.
    :param geneset_score_type: An instance of GenesetScoreType, representing the new
    threshold to set.
    :return:  A query (and params) that can be executed on a cursor.
    """
    if (
        geneset_score_type.threshold_low
        and geneset_score_type.threshold_low > geneset_score_type.threshold
    ):
        raise ValueError(
            "geneset_score_type.threshold must be larger than "
            "geneset_score_type.threshold_low"
        )

    params = {
        "geneset_id": geneset_id,
        "score_type": int(geneset_score_type.score_type),
        "threshold_str": geneset_score_type.threshold_as_db_string(),
    }
    query = (
        SQL("UPDATE geneset")
        + SQL("SET gs_threshold_type = %(score_type)s,")
        + SQL("gs_threshold = %(threshold_str)s")
        + SQL("WHERE gs_id = %(geneset_id)s;")
    )

    query = query.join(" ")

    return query, params


def set_geneset_value_threshold(
    geneset_id: int,
    geneset_score_type: GenesetScoreType,
) -> Tuple[Composed, dict]:
    """Update the threshold a geneset values.

    :param geneset_id: The ID of the geneset to update.
    :param geneset_score_type: An instance of GenesetScoreType, representing the new
    threshold to set.
    :return:  A query (and params) that can be executed on a cursor.
    """
    params = {
        "geneset_id": geneset_id,
        "threshold_high": geneset_score_type.threshold,
    }

    query = SQL(
        """
        UPDATE geneset_value
            SET gsv_in_threshold = CASE
        """
    )
    if geneset_score_type.threshold_low is not None:
        query = query + SQL(
            """
            WHEN gsv_value BETWEEN %(threshold_low)s AND %(threshold_high)s THEN TRUE
            """
        )
        params["threshold_low"] = geneset_score_type.threshold_low

        if geneset_score_type.threshold_low > geneset_score_type.threshold:
            raise ValueError(
                "geneset_score_type.threshold must be larger than "
                "geneset_score_type.threshold_low"
            )

    else:
        query = query + SQL(
            """
            WHEN gsv_value < %(threshold_high)s THEN TRUE
            """
        )

    query = query + SQL(
        """
                ELSE FALSE
            END
        WHERE gs_id = %(geneset_id)s;
        """
    )

    query = query.join(" ")

    return query, params


def user_can_set_threshold(user_id: int, geneset_id: int) -> Tuple[Composed, dict]:
    """Check if a user can set the threshold of a geneset.

    A user can set the threshold of a geneset if:
        - They own the Geneset, or
        - They are an admin, or
        - They are a curator, or
        - They are assigned curation on the geneset.

    :param user_id: The ID of the user to check.
    :param geneset_id: The ID of the geneset to check.
    :return: A query (and params) that can be executed on a cursor.
    """
    params = {"user_id": user_id, "geneset_id": geneset_id}
    query = (
        SQL("SELECT EXISTS(")
        + SQL("SELECT 1")
        + SQL("FROM geneset g")
        + SQL("WHERE g.gs_id = %(geneset_id)s")
        +
        # The user must either
        # 1) own the geneset, or
        SQL("AND g.usr_id = %(user_id)s")
        +
        # 2) be a curator or an admin, or
        SQL("OR")
        + user.is_curator_or_higher__query()
        +
        # 3) be assigned curation on the geneset.
        SQL("OR")
        + user.is_assigned_curation__query()
        + SQL(");")
    ).join(" ")
    return query, params
