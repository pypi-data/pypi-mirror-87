import math
import time
from functools import wraps
from sqlalchemy import desc


class QueryStatus:
    def __init__(self, table, function, data=None, elapsed_time=None):
        self.table = table
        self.function = function
        self.data = data
        self.elapsed_time = elapsed_time

    def __repr__(self):
        return "Table: {}, Query: {}, Elapsed Time: {} [s]".format(
            self.table, self.function, self.elapsed_time)

    @staticmethod
    def get_query_status(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            st = time.clock()
            model_svc, data = fn(*args, **kwargs)
            et = time.clock() - st
            qs = QueryStatus(table=model_svc.table.__name__,
                             function=fn.__name__,
                             data=data,
                             elapsed_time=et)
            return qs
        return wrapper


class RecordsPage:
    def __init__(self, num_records, page_records, per_page=None, current_page=None):
        self.num_records = num_records
        self.page_records = page_records
        self.per_page = per_page
        self.current_page = current_page
        self.num_pages = math.ceil(num_records / per_page) if per_page else None
