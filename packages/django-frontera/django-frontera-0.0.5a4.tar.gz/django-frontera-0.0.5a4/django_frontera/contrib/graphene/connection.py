import binascii
import warnings
from typing import Any, Optional, Sequence

from graphql_relay.connection.connectiontypes import (
    Connection,
    Edge,
)
from graphql_relay.connection.arrayconnection import (
    offset_to_cursor,
    get_offset_with_default,
)

from .connectiontypes import PageInfo

def connection_from_array(
    data: Sequence,
    args = None,
    connection_type: Any = Connection,
    edge_type: Any = Edge,
    page_info_type: Any = PageInfo,
) -> Connection:
    """Create a connection object from a sequence of objects.
    Note that different from its JavaScript counterpart which expects an array,
    this function accepts any kind of sliceable object with a length.
    Given this `data` object representing the result set, and connection arguments,
    this simple function returns a connection object for use in GraphQL. It uses
    offsets as pagination, so pagination will only work if the data is static.
    The result will use the default types provided in the `connectiontypes` module
    if you don't pass custom types as arguments.
    """
    offset = args.get("offset", 0)

    return connection_from_array_slice(
        data,
        args,
        slice_start=offset,
        array_length=len(data),
        connection_type=connection_type,
        edge_type=edge_type,
        page_info_type=page_info_type,
    )

def connection_from_array_slice(
    array_slice: Sequence,
    args = None,
    slice_start: int = 0,
    array_length: int = None,
    array_slice_length: int = None,
    connection_type: Any = Connection,
    edge_type: Any = Edge,
    page_info_type: Any = PageInfo,
) -> Connection:
    """Create a connection object from a slice of the result set.
    Note that different from its JavaScript counterpart which expects an array,
    this function accepts any kind of sliceable object. This object represents
    a slice of the full result set. You need to pass the start position of the
    slice as `slice start` and the length of the full result set as `array_length`.
    If the `array_slice` does not have a length, you need to provide it separately
    in `array_slice_length` as well.
    This function is similar to `connection_from_array`, but is intended for use
    cases where you know the cardinality of the connection, consider it too large
    to materialize the entire result set, and instead wish to pass in only a slice
    of the total result large enough to cover the range specified in `args`.
    If you do not provide a `slice_start`, we assume that the slice starts at
    the beginning of the result set, and if you do not provide an `array_length`,
    we assume that the slice ends at the end of the result set.
    """
    args = args or {}
    before = args.get("before")
    after = args.get("after")
    first = args.get("first")
    last = args.get("last")
    if array_slice_length is None:
        array_slice_length = len(array_slice)
    slice_end = slice_start + array_slice_length
    if array_length is None:
        array_length = slice_end
    before_offset = get_offset_with_default(before, array_length)
    after_offset = get_offset_with_default(after, -1)

    start_offset = max(slice_start - 1, after_offset, -1) + 1
    end_offset = min(slice_end, before_offset, array_length)

    if isinstance(first, int):
        if first < 0:
            raise ValueError("Argument 'first' must be a non-negative integer.")

        end_offset = min(end_offset, start_offset + first)
    if isinstance(last, int):
        if last < 0:
            raise ValueError("Argument 'last' must be a non-negative integer.")

        start_offset = max(start_offset, end_offset - last)

    # If supplied slice is too large, trim it down before mapping over it.
    trimmed_slice = array_slice[
        start_offset - slice_start : array_slice_length - (slice_end - end_offset)
    ]

    edges = [
        edge_type(node=value, cursor=offset_to_cursor(start_offset + index))
        for index, value in enumerate(trimmed_slice)
    ]

    first_edge_cursor = edges[0].cursor if edges else None
    last_edge_cursor = edges[-1].cursor if edges else None
    lower_bound = after_offset + 1 if after else 0
    upper_bound = before_offset if before else array_length

    return connection_type(
        edges=edges,
        pageInfo=page_info_type(
            startCursor=first_edge_cursor,
            endCursor=last_edge_cursor,
            hasPreviousPage=isinstance(last, int) and start_offset > lower_bound,
            hasNextPage=isinstance(first, int) and end_offset < upper_bound,
            totalCount=array_slice_length,
        ),
    )