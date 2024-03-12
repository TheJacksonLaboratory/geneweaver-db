from typing import Dict, Optional, Union, Tuple, List
from psycopg.sql import SQL, Composed

SQLList = List[Union[Composed, SQL]]
ParamDict = Dict[str, Union[str, int]]
OptionalParamDict = Dict[str, Optional[Union[str, int]]]


def construct_filter(
    filters: SQLList,
    params: ParamDict,
    filter_name: str,
    filter_value: Optional[Union[str, int]],
) -> Tuple[SQLList, ParamDict]:
    if filter_value is not None:
        filters.append(
            SQL("{filter_name} = %({filter_name})s").format(filter_name)
        )
        params[filter_name] = filter_value
    return filters, params


def construct_filters(
        filters: SQLList,
        params: ParamDict,
        filter_items: OptionalParamDict,
) -> Tuple[SQLList, ParamDict]:
    for filter_name, filter_value in filter_items.items():
        filters, params = construct_filter(
            filters,
            params,
            filter_name,
            filter_value,
        )

    return filters, params
