"""Utility functions for the SQL generation functions."""

from typing import Dict, List, Optional, Tuple, Union

from geneweaver.db.query.search import utils as search_utils
from psycopg.sql import SQL, Composed, Identifier, Placeholder

SQLList = List[Union[Composed, SQL]]
ParamDict = Dict[str, Union[str, int, list]]
OptionalParamDict = Dict[str, Optional[Union[str, int]]]


def construct_filter(
    filters: SQLList,
    params: ParamDict,
    filter_name: str,
    filter_value: Optional[Union[str, int]],
) -> Tuple[SQLList, ParamDict]:
    """Construct a simple filter for a query.

    :param filters: The existing filters.
    :param params: The existing parameters.
    :param filter_name: The filter name to construct.
    :param filter_value: The filter value to construct.

    :return: The constructed filters and parameters.
    """
    if filter_value is not None:
        filters.append(
            SQL("{filter_name} = {param_name}").format(
                filter_name=Identifier(filter_name), param_name=Placeholder(filter_name)
            )
        )
        params[filter_name] = filter_value
    return filters, params


def construct_filters(
    filters: SQLList,
    params: ParamDict,
    filter_items: OptionalParamDict,
) -> Tuple[SQLList, ParamDict]:
    """Construct multiple simple filters for a query.

    Calls the `construct_filter` function for each filter item.

    :param filters: The existing filters.
    :param params: The existing parameters.
    :param filter_items: The filter items to construct.

    :return: The constructed filters and parameters.
    """
    for filter_name, filter_value in filter_items.items():
        filters, params = construct_filter(
            filters,
            params,
            filter_name,
            filter_value,
        )

    return filters, params


def search(
    field_ts_vector: str,
    existing_filters: SQLList,
    existing_params: ParamDict,
    search_text: Optional[str] = None,
) -> Tuple[SQLList, ParamDict]:
    """Add the search filter to the query.

    :param field_ts_vector: proj_tsvector column in db table
    :param existing_filters: The existing filters.
    :param existing_params: The existing parameters.
    :param search_text: The search text to filter by.
    """
    if search_text is not None:
        search_sql, search_params = search_utils.search_query(
            field_ts_vector, search_text
        )
        existing_filters.append(search_sql)
        existing_params.update(search_params)
    return existing_filters, existing_params
