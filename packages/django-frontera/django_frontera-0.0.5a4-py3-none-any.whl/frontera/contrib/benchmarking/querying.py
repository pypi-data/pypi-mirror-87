from time import time as timer
import logging

logger = logging.getLogger(__name__)

def log_db_queries(f):
    from django.db import connection
    from functools import reduce

    def new_f(*args, **kwargs):
        res = f(*args, **kwargs)
        print("-" * 80)
        print("db queries log for %s:\n" % (f.__name__))
        print("TOTAL COUNT: %s" % len(connection.queries))
        print("TOTAL TIME:  %s\n" % reduce(lambda x, y: x + float(y["time"]), connection.queries, 0.0))
        for q in connection.queries:
            print("%s:  %s\n" % (q["time"], q["sql"]))
        print("-" * 80)
        return res
    return new_f


def GrapheneTimingMiddleware(next, root, info, **args):
    start = timer()
    return_value = next(root, info, **args)
    duration = timer() - start
    logger.debug("{parent_type}.{field_name}: {duration} ms".format(
        parent_type=root._meta.name if root and hasattr(root, '_meta') else '',
        field_name=info.field_name,
        duration=round(duration * 1000, 2)
    ))
    return return_value
