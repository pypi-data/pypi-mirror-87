import logging
from graphql import GraphQLError

class GraphQLLogFilter(logging.Filter):
    def filter(self, record):
        if 'graphql.error.located_error.GraphQLLocatedError:' in record.msg:
            return False
        return True
