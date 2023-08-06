from functools import partial

import graphene
from .connection import connection_from_array, PageInfo

class PageInfo(graphene.relay.PageInfo):
    class Meta:
        description = (
            "The Relay compliant `PageInfo` type, containing data necessary to"
            " paginate this connection + some Frontera fields"
        )

    total_count = graphene.Int(
        required=True,
        name="totalCount",
        description="What is the total number of items?")


def page_info_adapter(startCursor, endCursor, hasPreviousPage, hasNextPage, totalCount):
    """Adapter for creating PageInfo instances"""
    return PageInfo(
        start_cursor=startCursor,
        end_cursor=endCursor,
        has_previous_page=hasPreviousPage,
        has_next_page=hasNextPage,
        totalCount=totalCount)


def connection_adapter(cls, edges, pageInfo):
    """Adapter for creating Connection instances"""
    return cls(edges=edges, page_info=pageInfo)


class ConnectionBase(graphene.relay.Connection):
    total_count = graphene.Int()

    class Meta:
        abstract = True

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()

class IterableConnectionField(graphene.types.Field):    
    def __init__(self, type, *args, **kwargs):
        kwargs.setdefault("before", String())
        kwargs.setdefault("after", String())
        kwargs.setdefault("first", Int())
        kwargs.setdefault("last", Int())
        kwargs.setdefault("offset", Int())
        super(IterableConnectionField, self).__init__(type, *args, **kwargs)
    
    @classmethod
    def resolve_connection(cls, connection_type, args, resolved):
        if isinstance(resolved, connection_type):
            return resolved

        assert isinstance(resolved, Iterable), (
            "Resolved value from the connection field has to be an iterable or instance of {}. "
            'Received "{}"'
        ).format(connection_type, resolved)
        connection = connection_from_array(
            resolved,
            args,
            connection_type=partial(connection_adapter, connection_type),
            edge_type=connection_type.Edge,
            page_info_type=page_info_adapter,
        )
        connection.iterable = resolved
        return connection