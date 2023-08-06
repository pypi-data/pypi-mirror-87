from . import QueryStatus
from sqlalchemy import desc, case


class TableService:
    def __init__(self, database, table=None, per_page=10, with_view=None):
        self.database = database
        self.table = table
        self.per_page = per_page
        self.with_view = with_view

    def query(self, row_filter=None, column_filter=list(), group_by=None, order_by=dict()):

        query = self.table.query

        # Rows filtering
        if row_filter is not None:
            row_filter = self.add_view(row_filter)
            query = query.filter(row_filter)

        # Columns filtering
        if len(column_filter) > 0:
            query = query.with_entities(*column_filter)

        # Grouping
        if group_by:
            query = query.group_by(group_by)

        # Ordering
        if len(order_by) > 0:
            req_col = order_by['column'] if order_by['ascending'] else desc(order_by['column'])

            if 'nulls_last' in order_by and order_by['nulls_last'] is True:
                query = query.order_by(case([(getattr(self.table, order_by['column']).is_(None), 1)],
                                            else_=0), req_col)
            else:
                query = query.order_by(req_col)

        return query

    @QueryStatus.get_query_status
    def read(self, row_filter=None, column_filter=list(), group_by=None, order_by=dict(),
             count='first', page=None):
        """ Return query records """

        query = self.query(row_filter, column_filter, group_by, order_by)

        if count == 'first':
            return self, query.first()

        if page is None:
            return self, query.all()

        else:
            pager = query.paginate(per_page=self.per_page, page=page)
            return self, {'page': pager.items, 'num_pages': pager.pages}

    @QueryStatus.get_query_status
    def count(self, row_filter=None, column_filter=list()):
        """ Return number of records per query """

        query = self.query(row_filter, column_filter)
        return self, query.count()

    @QueryStatus.get_query_status
    def is_available(self, row_filter):
        """ Check if a record is available """

        qs = self.count(row_filter)
        return self, qs.data > 0

    @QueryStatus.get_query_status
    def create(self, new_record, with_commit=True):
        """ Create a new record
            new_record: is an object of the model type
        """

        self.database.session.add(new_record)
        if with_commit:
            self.commit()
        return self, None

    @QueryStatus.get_query_status
    def update(self, _id, updated_record, with_commit=True):
        """ Update an existing record
            updated_record: is a dictionary
        """

        query = self.query(self.table.id == _id)
        query.update(updated_record)
        if with_commit:
            self.commit()
        return self, None

    @QueryStatus.get_query_status
    def delete(self, _id, with_commit=True):
        """ Delete an existing record """

        qs = self.read(self.table.id == _id)
        self.database.session.delete(qs.data)
        if with_commit:
            self.commit()
        return self, None

    def commit(self):
        try:
            self.database.session.commit()

        except Exception as e:
            self.database.session.rollback()
            raise e

    def add_view(self, row_filter):
        if self.with_view is not None:
            return row_filter & self.with_view if row_filter is not None else self.with_view
        return row_filter
